# -*- coding: utf-8 -*-
import argparse
import hione
import lib

global_config = lib.getConfigByJsonFile("/home/pi/www/python/config.json")


def main():
    global global_config

    cmds = ["isDoorOpen", "doorOpenProcess", "doorCloseProcess"]

    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("cmd", choices=cmds, help="bar help")
    parser.add_argument(
        "-p",
        "--port",
        help="Hione doorlock serial port number",
        default=global_config["doorlock"],
    )

    args = parser.parse_args()

    if not args.port:
        print("Error: Port number must be provided with -p or --port.")
        return

    obj = hione.Hione(port=args.port)

    if args.cmd == "isDoorOpen":
        results = dict()
        results["result"] = obj.isDoorOpen()
        rs = lib.jsonencode(results)
        print(rs)
    elif args.cmd == "doorOpenProcess":
        results = dict()
        results["result"] = obj.doorOpenProcess()
        rs = lib.jsonencode(results)
        print(rs)
    elif args.cmd == "doorCloseProcess":
        results = dict()
        results["result"] = obj.doorOpenProcess()
        rs = lib.jsonencode(results)
        print(rs)


if __name__ == "__main__":
    main()
