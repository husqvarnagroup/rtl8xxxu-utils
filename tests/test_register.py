import pytest

from rtl8xxxu.register import _parse_rtl8xxxu_reg_header_extract, PartialRegisterDescription, FieldDescription, \
    NAME_TO_REGULAR_REGISTER_SECTION, RegisterDescription, RegisterMap, NAME_TO_RF_REGISTER_SECTION, RegisterSection, \
    NAME_TO_ANY_REGISTER_SECTION


def test__parse_rtl8xxxu_reg_header_extract():
    test_header_regular = """
#define REG_RXERR_RPT			0x0664
#define  RXERR_RPT_RESET		BIT(27)
#define  RXERR_RPT_CTR_TYPE_MASK	0xf0000000
#define REG_WMAC_TRXPTCL_CTL		0x0668
#define  WMAC_TRXPTCL_CTL_BW_MASK	(BIT(7) | BIT(8))
#define  WMAC_TRXPTCL_CTL_BW_20		0
#define REG_CAM_CMD			0x0670
#define  NON_CONTINUOUS_MASK	0x101
"""
    assert _parse_rtl8xxxu_reg_header_extract("") == ([], [])

    registers, fields = _parse_rtl8xxxu_reg_header_extract(test_header_regular)
    assert sorted(registers) == sorted([
        PartialRegisterDescription("REG_RXERR_RPT", 0x0664),
        PartialRegisterDescription("REG_WMAC_TRXPTCL_CTL", 0x0668),
        PartialRegisterDescription("REG_CAM_CMD", 0x670),
    ])
    assert fields == [
        FieldDescription.from_range('RXERR_RPT_RESET', 27, 28),
        FieldDescription.from_range('RXERR_RPT_CTR_TYPE', 28, 32),
        # Mask WMAC_TRXPTCL_CTL_BW_MASK must get ignored
        FieldDescription('NON_CONTINUOUS', 0x101),
    ]

    with pytest.raises(RuntimeError, match='Duplicates in bit mask:'):
        _parse_rtl8xxxu_reg_header_extract('#define  DUPLICATES	(BIT(7) | BIT(8) | BIT(7))')


class TestPartialRegisterDescription:
    def test_is_of_type_positive(self):
        assert PartialRegisterDescription('REG_BSSID1', 0x0708).is_of_type(NAME_TO_REGULAR_REGISTER_SECTION['MAC'])
        assert PartialRegisterDescription('REG_FPGA0_RF_MODE', 0x800).is_of_type(NAME_TO_REGULAR_REGISTER_SECTION['BB'])
        assert PartialRegisterDescription('RF6052_REG_RCK_OS', 0x30).is_of_type(NAME_TO_RF_REGISTER_SECTION['RF'])

    def test_is_of_type_negative(self):
        assert not PartialRegisterDescription('REG_BSSID1', 0x0708).is_of_type(NAME_TO_RF_REGISTER_SECTION['RF'])
        assert not PartialRegisterDescription('REG_FPGA0_RF_MODE', 0x800).is_of_type(
            NAME_TO_REGULAR_REGISTER_SECTION['MAC'])
        assert not PartialRegisterDescription('RF6052_REG_RCK_OS', 0x30).is_of_type(
            NAME_TO_REGULAR_REGISTER_SECTION['BB'])


class TestFieldDescription:
    def test_belongs_to(self):
        r = PartialRegisterDescription('REG_WMAC_TRXPTCL_CTL', 0x0668)
        assert FieldDescription.from_range('WMAC_TRXPTCL_CTL_BW', 7, 9).belongs_to(r)


class TestRegisterDescription:
    def test_add_register_regular(self):
        rm = RegisterMap(NAME_TO_REGULAR_REGISTER_SECTION['MAC'])
        reg1 = rm.add_register(PartialRegisterDescription('REG_MACID1', 0x0700))
        reg2 = rm.add_register(PartialRegisterDescription('REG_BSSID1', 0x0708))
        assert rm.next_register(reg1) == reg2
        assert reg1.parent == reg2.parent == rm
        assert reg1._next_register_description == reg2
        assert rm.register_at_address(0x0709) == reg2
        assert rm.register_at_address(0x070a) == reg2
        assert rm.register_at_address(0x070b) == reg2
        assert rm.register_at_address(0x070c).name == 'unknown'

    def test_size_regular(self):
        rm = RegisterMap(NAME_TO_REGULAR_REGISTER_SECTION['MAC'])
        reg_at_0 = rm.add_register(PartialRegisterDescription('REG_0', 0x00))
        reg_at_1 = rm.add_register(PartialRegisterDescription('REG_1', 0x01))
        assert reg_at_1.length == 3
        assert reg_at_1.depth == 1
        reg_at_3 = rm.add_register(PartialRegisterDescription('REG_3', 0x03))
        assert reg_at_1.length == 2
        assert reg_at_1.depth == 1
        assert reg_at_3.length == 1
        assert reg_at_3.depth == 1
        assert rm.register_at_address(0x04).name == 'unknown'

    def test_add_register_rf(self):
        rm = RegisterMap(NAME_TO_ANY_REGISTER_SECTION['RF'])
        reg1 = rm.add_register(PartialRegisterDescription('RF6052_REG_SYN_G7', 0x2b))
        reg2 = rm.add_register(PartialRegisterDescription('RF6052_REG_SYN_G8', 0x2c))
        assert rm.next_register(reg1) == reg2
        assert reg1.parent == reg2.parent == rm
        assert reg1._next_register_description == reg2
        assert rm.register_at_address(0x2d).name == 'unknown'

    def test_size_rf(self):
        rm = RegisterMap(NAME_TO_ANY_REGISTER_SECTION['RF'])
        reg_at_0 = rm.add_register(PartialRegisterDescription('RF6052_REG_SYN_G1', 0x25))
        reg_at_1 = rm.add_register(PartialRegisterDescription('RF6052_REG_SYN_G2', 0x26))
        assert reg_at_0.length == reg_at_1.length == 1
        assert reg_at_0.depth == reg_at_1.depth == 4

    def test_with_fields(self):
        rm = RegisterMap(NAME_TO_REGULAR_REGISTER_SECTION['MAC'])
        reg = RegisterDescription(rm, 'Register', 0x0)
        assert reg.known_bitmask == 0
        field_0 = FieldDescription.from_range("Bit 0", 0, 1)
        reg.add_field(field_0)
        field_3 = FieldDescription.from_range("Bit 3-4", 3, 5)
        reg.add_field(field_3)
        field_1 = FieldDescription.from_range("Bit 1", 1, 2)
        reg.add_field(field_1)
        assert reg.known_bitmask == 0b11011
        with pytest.raises(RuntimeError):
            reg.add_field(FieldDescription.from_range("Bit 4-5", 4, 6))
        assert reg.known_fields == [field_0, field_1, field_3]
        assert reg.get_affected_fields(0b1001) == [FieldDescription('Bit 0', 0x1),
                                                   FieldDescription('Bit 3-4', 0b11000)]


class TestRegisterSection:
    def test_compare(self):
        assert RegisterSection('MAC', 0, 0x800, 1, 4, 'REG_', 16) == NAME_TO_REGULAR_REGISTER_SECTION['MAC']
        assert RegisterSection('SECTION 1', 0, 0x800, 1, 4, 'REG_', 16) != RegisterSection('SECTION 2', 0, 0x800, 1,
                                                                                           4, 'REG_', 16)


@pytest.fixture
def register_map_rf() -> RegisterMap:
    header = """
/* RF6052 registers */
#define RF6052_REG_AC			0x00
#define RF6052_REG_IQADJ_G1		0x01
#define RF6052_REG_IQADJ_G2		0x02
#define RF6052_REG_BS_PA_APSET_G1_G4	0x03
"""
    return RegisterMap.from_rtl8xxxu_header(header, NAME_TO_RF_REGISTER_SECTION['RF'])


def test_bitmask(register_map_rf):
    r = RegisterDescription(register_map_rf, 'BS_PA_APSET_G1_G4', 0x3)
    assert r.size == 4
    assert r.bitmask == 0xFFFFFFFF
