# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import copy
from functools import lru_cache
from typing import TYPE_CHECKING, TypeVar

T = TypeVar("T")


def copy_with(obj: T, **kwargs) -> T:
    """Return copy of `obj` and update attributes of the copy using `kwargs`.

    ::

        @dataclass
        class MyClass:
            value: int

        a = MyClass(1)
        b = copy_with(a, value=2)

        assert a.value == 1
        assert b.value == 2

    """

    new_obj = copy.copy(obj)

    for name, value in kwargs.items():
        setattr(new_obj, name, value)

    return new_obj


if TYPE_CHECKING:
    lazy_property = property

else:

    def lazy_property(method):
        """Property that is lazily evaluated.

        This is the same as::

            @property
            @lru_cache(1)
            def my_property(self):
                ...

        In addition to be more concise, `lazy_property` also works with mypy,
        since it poses to be just `property` when type checked.

        This implementation follows the recipe from the `functools`
        documentation, and mimics `functools.cached_property` which was
        introduced in Python 3.8.
        """
        return property(lru_cache(1)(method))
