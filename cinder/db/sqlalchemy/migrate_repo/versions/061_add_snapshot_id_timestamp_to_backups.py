# Copyright (c) 2015 EMC Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Column, DateTime, MetaData, String, Table


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    backups = Table('backups', meta, autoload=True)
    snapshot_id = Column('snapshot_id', String(length=36))
    data_timestamp = Column('data_timestamp', DateTime)

    backups.create_column(snapshot_id)
    backups.update().values(snapshot_id=None).execute()

    backups.create_column(data_timestamp)
    backups.update().values(data_timestamp=None).execute()

    # Copy existing created_at timestamp to data_timestamp
    # in the backups table.
    backups_list = list(backups.select().execute())
    for backup in backups_list:
        backup_id = backup.id
        backups.update().\
            where(backups.c.id == backup_id).\
            values(data_timestamp=backup.created_at).execute()
