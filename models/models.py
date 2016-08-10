# -*- coding: utf-8 -*-

#     Odoo-S3
#     Allows you to use Odoo with AWS S3 buckets for file storage.
#     Copyright (C) 2016  Thomas Vanesse
#
#     This program is partly based on a legacy addon written by
#     Hugo Santos <hugo.santos@factolibre.com> in 2014 for Odoo v7.0.
#     The original module and source code can found here:
#       https://www.odoo.com/apps/modules/7.0/document_amazons3/

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from openerp import models

from openerp.osv import osv

import boto
import base64
import hashlib


class S3Attachment(osv.osv):
    """Extends ir.attachment to implement the S3 storage engine
    """
    _inherit = "ir.attachment"

    def _connect_to_S3_bucket(self, bucket_url):
        # Parse the bucket url
        scheme = bucket_url[:5]
        assert scheme == 's3://', \
            "Expecting an s3:// scheme, got {} instead.".format(scheme)

        try:
            remain = bucket_url.lstrip(scheme)
            access_key_id = remain.split(':')[0]
            remain = remain.lstrip(access_key_id).lstrip(':')
            secret_key = remain.split('@')[0]
            bucket_name = remain.split('@')[1]
            if not access_key_id or not secret_key:
                raise Exception(
                    "No AWS access and secret keys were provided."
                    " Unable to establish a connexion to S3."
                )
        except Exception:
            raise Exception("Unable to parse the S3 bucket url.")

        s3_conn = boto.connect_s3(access_key_id, secret_key)
        s3_bucket = s3_conn.lookup(bucket_name)
        if not s3_bucket:
            # If the bucket does not exist, create a new one
            s3_bucket = s3_conn.create_bucket(bucket_name)

        return s3_bucket

    def _file_read(self, cr, uid, fname, bin_size=False):
        storage = self._storage(cr, uid)
        if storage[:5] == 's3://':
            s3_bucket = self._connect_to_S3_bucket(storage)
            s3_key = s3_bucket.get_key(fname)
            if not s3_key:
                # Some old files (prior to the installation of odoo-S3) may
                # still be stored in the file system even though
                # ir_attachment.location is configured to use S3
                try:
                    read = super(S3Attachment, self)._file_read(cr, uid, fname, bin_size=False)
                except Exception:
                    # Could not find the file in the file system either.
                    return False
            else:
                read = base64.b64encode(s3_key.get_contents_as_string())
        else:
            read = super(S3Attachment, self)._file_read(cr, uid, fname, bin_size=False)
        return read

    def _file_write(self, cr, uid, value, checksum):
        storage = self._storage(cr, uid)
        if storage[:5] == 's3://':
            s3_bucket = self._connect_to_S3_bucket(storage)
            bin_value = value.decode('base64')
            fname = hashlib.sha1(bin_value).hexdigest()

            s3_key = s3_bucket.get_key(fname)
            if not s3_key:
                s3_key = s3_bucket.new_key(fname)

            s3_key.set_contents_from_string(bin_value)
        else:
            fname = super(S3Attachment, self)._file_write(
                cr, uid, value, checksum)

        return fname
