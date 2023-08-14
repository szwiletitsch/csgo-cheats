from json import loads
from hackingPackage.memoryAccess import *


with open("data/offsets.json", "rt") as f:
    a = f.read()
    signatures = loads(a)["signatures"]
    net_vars = loads(a)["netvars"]


# get handle and modules
handle = get_handle_and_open_process_by_name("Counter-Strike: Global Offensive - Direct3D 9")
client_dll = get_module("client.dll", handle)
engine_dll = get_module("engine.dll", handle)
client_state_ptr = handle.read_bytes(engine_dll + signatures["dwClientState"], 4)
client_state_ptr = int.from_bytes(client_state_ptr, byteorder='little')


class Player:
    def __init__(self, pointer):
        self.base = pointer

    def get_pos(self):
        return read_vec(handle, self.base + net_vars["m_vecOrigin"])

    def get_view_offset(self):
        return read_vec(handle, self.base + net_vars["m_vecViewOffset"])

    def get_team(self):
        return handle.read_int(self.base + net_vars["m_iTeamNum"])

    def get_health(self):
        return handle.read_int(self.base + net_vars["m_iHealth"])

    def get_bone_pos(self, bone):
        bone_matrix_ptr = handle.read_int(self.base + net_vars["m_dwBoneMatrix"])
        x = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x0C)
        y = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x1C)
        z = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x2C)
        return Vec3(x, y, z)

    def get_head_pos(self):
        return self.get_bone_pos(8)


class LocalPlayer:
    def __init__(self):
        self.base = handle.read_int(client_dll + signatures["dwLocalPlayer"])

    def get_team(self):
        return handle.read_int(self.base + net_vars["m_iTeamNum"])

    def get_health(self):
        return handle.read_int(self.base + net_vars["m_iHealth"])

    def get_pos(self):
        return read_vec(handle, self.base + net_vars["m_vecOrigin"])

    def get_view_offset(self):
        return read_vec(handle, self.base + net_vars["m_vecViewOffset"])

    def get_bone_pos(self, bone):
        bone_matrix_ptr = handle.read_int(self.base + net_vars["m_dwBoneMatrix"])
        x = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x0C)
        y = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x1C)
        z = handle.read_float(bone_matrix_ptr + 0x30 * bone + 0x2C)
        return Vec3(x, y, z)

    def get_head_pos(self):
        return self.get_bone_pos(8)

    def get_view_angles(self):
        return read_vec(handle, client_state_ptr + signatures["dwClientState_ViewAngles"])

    def set_view_angle(self, vec: Vec3):
        vec = vec.validate_view_angles()
        write_vec(handle, client_state_ptr + signatures["dwClientState_ViewAngles"], vec.load())

    def get_view_matrix(self):
        matrix = []
        for i in range(16):
            matrix.append(handle.read_float(client_dll + signatures["dwViewMatrix"] + i*4))
        return matrix


def get_players():
    max_players = handle.read_int(client_state_ptr + signatures["dwClientState_MaxPlayer"])
    list_of_players = []
    for increment in range(max_players):
        cur_player = client_dll + signatures["dwEntityList"] + increment * 0x10
        player_ptr = handle.read_int(cur_player)
        if player_ptr != 0:
            list_of_players.append(Player(player_ptr))
    return list_of_players


def world_to_screen(point: Vec3, view_matrix=None):
    if not view_matrix:
        view_matrix = LocalPlayer().get_view_matrix()

    p0 = view_matrix[0] * point.x + view_matrix[1] * point.y + view_matrix[2] * point.z + view_matrix[3]
    p1 = view_matrix[4] * point.x + view_matrix[5] * point.y + view_matrix[6] * point.z + view_matrix[7]
    p2 = view_matrix[12] * point.x + view_matrix[13] * point.y + view_matrix[14] * point.z + view_matrix[15]

    if p2 < 0.01:
        return False

    p0 = p0 / p2
    p1 = p1 / p2

    x = (960 * p0) + (p0 + 960)
    y = (540*p1) + (p1 + 540)
    return x, y
