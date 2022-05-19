#!/usr/bin/env python

# Copyright 2022 Kaiyu Zheng
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Visit every node of a topological graph

import rospy
from search_in_region import get_param
from action.waypoint import WaypointApply
from topo_marker_publisher import PublishTopoMarkers

def main():
    rospy.init_node("movo_topo_map_visitor",
                    anonymous=True)
    topo_map_file = get_param('topo_map_file')
    # don't actually publish; it's already published    
    pub = PublishTopoMarkers(topo_map_file, 0.3)
    
    waypoints = []
    i = 0
    for nid in sorted(pub.nodes):
        posit = pub.nodes[nid]
        orien = (0,0,0,1)
        waypoints.append(((posit, orien), nid))
        rospy.loginfo("[%d] Node %d, %s" % (i, nid, str(posit)))
        i += 1

    i = 0
    for goal, nid in waypoints:
        posit, orien = goal
        rospy.loginfo("Navigating to Node %d at %s [step %d]" % (nid, str(goal), i))
        if WaypointApply(posit, orien).status != WaypointApply.Status.SUCCESS:
            rospy.logerr("Waypoint to %d failed" % nid)
            break
        i += 1
    rospy.loginfo("All done!")
    
if __name__ == "__main__":
    main()

# command to run:
#    rosrun movo_object_search search_in_region.py _regions:="table-area,desktop-area,shelf-corner,whiteboard-area"
