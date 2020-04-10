from antimait.plotting import format_filename
import antimait
import datetime
import pathlib
import logging

logging.basicConfig(level=logging.INFO)


class Logger(antimait.DataReceiver):
    
    def __init__(self, filename: str, gw: antimait.Gateway, device: str):
        self._filename = filename
        self._device = device
        self._gw = gw

    def _append(self, msg: str):
        with open(self._filename, "a") as file:
            file.write("{}\n".format(msg))

    def _set_presence(self, presence: bool) -> str:
        presence = "start" if presence else "end"
        timestamp = datetime.datetime.now().strftime("%d-%m-%y_%I-%M-%S")
        msg = "Presence\t{}\t{}".format(presence, timestamp)
        self._append(msg)
        return timestamp

    def update(self, action: antimait.Comm, **update: str):
        if action == antimait.Comm.DATA:
            try:
                presence = update["data"].strip()
            except KeyError:
                raise KeyError("You need to specify the data keyword")
            
            if presence not in {"on", "off"}:
                raise ValueError("presence can only be 'on' or 'off'")
            presence_val = True if presence == "on" else False
            timestamp = self._set_presence(presence_val)
            timestamp = timestamp[timestamp.index("_")+1:].replace("-", ":")
            msg = "{} {}".format(presence, timestamp)
            self._gw.forward(self._device, msg)

if __name__ == "__main__":
    gw = antimait.Gateway()

    def on_connect(interface: antimait.CommInterface, description: str):
        logger = Logger(format_filename(description), gw, interface.ifc_id)
        interface.attach(logger)


    gw.on_connect = on_connect

    try:
        gw.listen_forever()
    except KeyboardInterrupt:
        gw.close()
        print("Bye!")