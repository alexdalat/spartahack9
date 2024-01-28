import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker

class WaypointWriter(Node):

    def __init__(self):
        super().__init__('waypoint_writer')
        self.subscription = self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.listener_callback,
            10)
        self.marker_publisher = self.create_publisher(Marker, '/waypoints_marker', 10)
        self.marker = Marker()
        self.initialize_marker()
        self.csv_file = open('waypoints.csv', mode='w')
        self.delimiter = ", "
        self.previous_point = None
        self.precision = 10  # Number of extra points to add

    def initialize_marker(self):
        self.marker.header.frame_id = "map"
        self.marker.type = Marker.LINE_STRIP
        self.marker.action = Marker.ADD
        self.marker.scale.x = 0.05  # Width of the line
        self.marker.scale.y = 0.1   # Size of the spheres
        self.marker.scale.z = 0.1
        self.marker.color.a = 1.0   # Alpha
        self.marker.color.r = 1.0   # Red
        self.marker.color.g = 0.0   # Green
        self.marker.color.b = 0.0   # Blue

    def interpolate_points(self, start, end, num_points):
        """Interpolate extra points between start and end."""
        points = []
        for i in range(1, num_points + 1):
            fraction = i / (num_points + 1)
            x = start.x + fraction * (end.x - start.x)
            y = start.y + fraction * (end.y - start.y)
            z = start.z + fraction * (end.z - start.z)
            points.append(Point(x=x, y=y, z=z))
        return points

    def listener_callback(self, msg):
        new_point = msg.point
        if self.previous_point is not None:
            # Generate interpolated points
            interpolated_points = self.interpolate_points(self.previous_point, new_point, self.precision)
            for point in interpolated_points:
                self.write_point_to_file(point)
                self.marker.points.append(point)
        
        self.write_point_to_file(new_point)
        self.marker.points.append(new_point)
        self.marker_publisher.publish(self.marker)
        self.previous_point = new_point

    def write_point_to_file(self, point):
        x, y = point.x, point.y
        w_tr_right_m = 1.1
        w_tr_left_m = 1.1
        line = f"{x}{self.delimiter}{y}{self.delimiter}{w_tr_right_m}{self.delimiter}{w_tr_left_m}\n"
        self.csv_file.write(line)
        self.csv_file.flush()
        self.get_logger().info(f'Writing to File: {line.strip()}')

    def __del__(self):
        self.csv_file.close()

def main(args=None):
    rclpy.init(args=args)
    waypoint_writer = WaypointWriter()
    rclpy.spin(waypoint_writer)
    waypoint_writer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
