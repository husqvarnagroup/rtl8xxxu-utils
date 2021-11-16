from register_dump import Dump, RawDump


class TestRegisterDump:
    def test_parse_dump_mac(self):
        mac_dump = """======= MAC REG (rtlwifi) =======
0x000: 0xBB1780AA 0x20010812 0x00207ca3 0x00000000
0x010: 0x49022b03 0x087be955 0x00400100 0x074d1100
0x020: 0x010f5505 0x0011800f 0x00ffdb83 0x000000ff
0x030: 0x8021faff 0x35008100 0x29000000 0x00002e22
0x040: 0x00080000 0x07880000 0x0000f000 0xDD8200CC"""

        reg_dump_content = Dump.parse_dump(RawDump('dummy', mac_dump))
        assert reg_dump_content.driver_name == 'rtlwifi'
        assert reg_dump_content.section.name == 'MAC'
        assert reg_dump_content.section.address_range_begin == 0x0
        assert reg_dump_content.address_to_value[0x00] == bytearray.fromhex('AA')
        assert reg_dump_content.address_to_value[0x03] == bytearray.fromhex('BB')
        assert reg_dump_content.address_to_value[0x4C] == bytearray.fromhex('CC')
        assert reg_dump_content.address_to_value[0x4F] == bytearray.fromhex('DD')
        assert reg_dump_content.size == 80

    def test_parse_dump_bb(self):
        bb_dump = """======= BB REG (rtl8xxxu) =======
0x800: 0x0004BBAA 0x00000001 0x0000fc00 0x0000000a"""

        reg_dump_content = Dump.parse_dump(RawDump('dummy', bb_dump))
        assert reg_dump_content.driver_name == 'rtl8xxxu'
        assert reg_dump_content.section.name == 'BB'
        assert reg_dump_content.section.address_range_begin == 0x800
        assert reg_dump_content.address_to_value[0x800] == bytearray.fromhex('AA')
        assert reg_dump_content.address_to_value[0x801] == bytearray.fromhex('BB')
        assert reg_dump_content.size == 16

    def test_parse_dump_rf(self):
        rf_dump = """======== RF REG (8192cu) =======
0x000: 0x00082e35 0x00031284 0x00098000 0x00018c63
0x004: 0x000210e7 0x000fc804 0x000f3200 0x0004a800
0x008: 0x000c8400 0x00060443 0x0001adb1 0x00054667"""

        reg_dump_content = Dump.parse_dump(RawDump('dummy', rf_dump))
        assert reg_dump_content.driver_name == '8192cu'
        assert reg_dump_content.section.name == 'RF'
        assert reg_dump_content.section.address_range_begin == 0x0
        assert reg_dump_content.address_to_value[0x0] == bytearray.fromhex('00082e35')
        assert reg_dump_content.address_to_value[0x1] == bytearray.fromhex('00031284')
        assert reg_dump_content.size == 4 * 3 * 4
