import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        self.publisher_ = self.create_publisher(Int32MultiArray, '/output/array', 10)
        self.sub1 = self.create_subscription(Int32MultiArray, '/input/array1', self.callback1, 10)
        self.sub2 = self.create_subscription(Int32MultiArray, '/input/array2', self.callback2, 10)
        self.array1 = []
        self.array2 = []

    def callback1(self, msg):
        self.array1 = msg.data
        self.maybe_publish()

    def callback2(self, msg):
        self.array2 = msg.data
        self.maybe_publish()

    def maybe_publish(self):
        if self.array1 and self.array2:
            merged = sorted(self.array1 + self.array2)
            msg = Int32MultiArray()
            msg.data = merged
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published merged array: {merged}')

def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
