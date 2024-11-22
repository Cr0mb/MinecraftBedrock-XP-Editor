import pymem
import pymem.process

pm = pymem.Pymem("Minecraft.Windows.exe")
base_address = pymem.process.module_from_name(pm.process_handle, "Minecraft.Windows.exe").lpBaseOfDll

base_pointer_offset = 0x06A4D1E8
offsets = [0xEE0, 0xE0, 0xE0, 0x300, 0x170, 0x8, 0x8, 0x8, 0x9C]

current_address = base_address + base_pointer_offset
for offset in offsets:
    current_address = pm.read_longlong(current_address) + offset

current_xp_value = pm.read_float(current_address)
print(f"Current XP value: {current_xp_value}")

new_xp_value = float(input("Enter the desired XP value: "))

pm.write_float(current_address, new_xp_value)
print(f"XP value updated to: {new_xp_value}")
