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

# This is referred from Redfish standard schema.
# http://redfish.dmtf.org/schemas/v1/Volume.v1_0_3.json

import logging

from sushy.resources import base
from sushy import utils

LOG = logging.getLogger(__name__)


class Volume(base.ResourceBase):
    """This class adds the Storage Volume resource"""

    identity = base.Field('Id', required=True)
    """The Volume identity string"""

    name = base.Field('Name')
    """The name of the resource"""

    capacity_bytes = base.Field('CapacityBytes', adapter=utils.int_or_none)
    """The size in bytes of this Volume."""


class VolumeCollection(base.ResourceCollectionBase):
    """This class represents the Storage Volume collection"""

    _volumes_sizes_bytes = None

    @property
    def _resource_type(self):
        return Volume

    @property
    def volumes_sizes_bytes(self):
        """Sizes of all Volumes in bytes in VolumeCollection resource.

        Returns the list of cached values until it (or its parent resource)
        is refreshed.
        """
        if self._volumes_sizes_bytes is None:
            self._volumes_sizes_bytes = sorted(
                vol.capacity_bytes
                for vol in self.get_members())
        return self._volumes_sizes_bytes

    @property
    def max_volume_size_bytes(self):
        """Max size available (in bytes) among all Volume resources.

        Returns the cached value until it (or its parent resource) is
        refreshed.
        """
        return utils.max_safe(self.volumes_sizes_bytes)

    # NOTE(etingof): for backward compatibility
    max_size_bytes = max_volume_size_bytes

    def _do_refresh(self, force=False):
        super(VolumeCollection, self)._do_refresh(force)
        # invalidate the attribute
        self._volumes_sizes_bytes = None
