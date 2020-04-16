# cython: language_level=3
#  Drakkar-Software OctoBot-Evaluators
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
from octobot_commons.event_tree cimport EventTreeNode
from octobot_evaluators.data.matrix cimport Matrix

cpdef Matrix get_matrix(str matrix_id)
cpdef void set_tentacle_value(str matrix_id, list tentacle_path, object tentacle_type,
                              object tentacle_value, double timestamp=*)
cpdef EventTreeNode get_tentacle_node(str matrix_id, list tentacle_path)
cpdef object get_tentacle_value(str matrix_id, list tentacle_path)
cpdef list get_matrix_default_value_path(str tentacle_name,
                                  object tentacle_type,
                                  str exchange_name=*,
                                  str cryptocurrency=*,
                                  str symbol=*,
                                  str time_frame=*)
cpdef list get_tentacle_nodes(str matrix_id, str exchange_name=*, object tentacle_type=*, str tentacle_name=*)
cpdef list get_tentacles_value_nodes(str matrix_id, list tentacle_nodes, str cryptocurrency=*, str symbol=*, str time_frame=*)
cpdef list get_tentacle_path(str exchange_name=*, object tentacle_type=*, str tentacle_name=*)
cpdef list get_tentacle_value_path(str cryptocurrency=*, str symbol=*, str time_frame=*)
cpdef bint is_tentacle_value_valid(str matrix_id, list tentacle_path, double timestamp=*, int delta=*)
cpdef bint is_tentacles_values_valid(str matrix_id, list tentacle_path_list, double timestamp=*, int delta=*)