from netmiko import ConnectHandler
import ntc_templates, os, json
from database import save_interface_status

def get_interfaces(ip, username, password):

    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )

    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
    }

    with ConnectHandler(**device) as conn:
        conn.enable()
        result = conn.send_command("show ip int br", use_textfsm=True)
        conn.disconnect()
    
    interface = json.loads(json.dumps(result, indent=2))
    save_interface_status(ip,interface)

if __name__=='__main__':
    get_interfaces()