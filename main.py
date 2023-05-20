from o_and_chaos import order_and_chaos
import argparse


def parse_arguments():
    """Parse argument needed to define game settings"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--role', required=True,
                        choices=['order', 'chaos'],
                        help='pick the role you want to play against AI')
    parser.add_argument('-ai', '--ai_type', required=True,
                        choices=['random', 'supreme'],
                        help='pick AI level of difficulty')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    order_and_chaos(args)
