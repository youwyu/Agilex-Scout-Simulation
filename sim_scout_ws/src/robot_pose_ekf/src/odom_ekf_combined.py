#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistWithCovarianceStamped

class OdomEKF():
    def __init__(self):
        self.Twist = TwistWithCovarianceStamped()
        # Give the node a name
        rospy.init_node('odom_ekf', anonymous=False)

        # Publisher of type nav_msgs/Odometry
        self.ekf_pub = rospy.Publisher('odom_ekf', Odometry, queue_size=10)
        
        # Wait for the /odom_combined topic to become available
        rospy.wait_for_message('odom_combined', PoseWithCovarianceStamped)
        
        # Subscribe to the /odom_combined topic
        rospy.Subscriber('odom', Odometry, self.TwistCallBack)
        rospy.Subscriber('odom_combined', PoseWithCovarianceStamped, self.pub_ekf_odom)
        
        rospy.loginfo("Publishing combined odometry on /odom_ekf")
        
    def pub_ekf_odom(self, msg):
        odom = Odometry()
        odom.header = msg.header
        odom.header.frame_id = '/odom_combined'
        odom.child_frame_id = 'base_link'
        odom.pose = msg.pose
        odom.twist = self.Twist.twist
        
        self.ekf_pub.publish(odom)
    
    def TwistCallBack(self,msg):
        self.Twist.header= msg.header
        self.Twist.twist = msg.twist
        
if __name__ == '__main__':
   try:
       OdomEKF()
       rospy.spin()
   except:
       pass