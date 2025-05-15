import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_07(self):
        input = [
            "INSERT x number",
            "INSERT y number",
            "ASSIGN y 100",
            "ASSIGN x y",
        ]
        expected = ["success", "success", "success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 107))

    def test_08(self):
        input = [
            " INSERT x number",
            "ASSIGN x 40",
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 108))

    def test_09(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT b string",
            "END",
            "BEGIN",
            "INSERT c number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "a//0 c//1"]
        
        self.assertTrue(TestUtils.check(input, expected, 109))

    def test_10(self):
        input = [
            "INSERT y@1 number",
        ]
        expected = ["Invalid: INSERT y@1 number"]
        
        self.assertTrue(TestUtils.check(input, expected, 110))

    def test_11(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'a@1'",
        ]
        expected = ["Invalid: ASSIGN x 'a@1'"]
        
        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_12(self):
        input = [
            "INSERT s string",
            "ASSIGN s ''",
        ]
        expected = ["success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 112))

    def test_13(self):
        input = [
            "INSERT a3 number",
            "ASSIGN a3 ASSIGN",
        ]
        expected = ["Invalid: ASSIGN a3 ASSIGN"]
        
        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = [
            "INSERT x string",
            "INSERT y string",
            "INSERT z number",
            "BEGIN",
            "ASSIGN x 'abc'",
            "INSERT x number",
            "ASSIGN x 50",
            "ASSIGN x 'def'",
            "ASSIGN z x",
            "END",
        ]
        expected = ["TypeMismatch: ASSIGN x 'def'"]
        
        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = [
            "INSERT number number",
        ]
        expected = ["success"]
        
        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = [
            "ASSIGN x 123.4"
        ]  
        expected = ["Undeclared: ASSIGN x 123.4"]
        
        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = [
            "PRINT",
            "RPRINT",
        ]
        expected = ["",""]
        
        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = [
            "INSERT a number",
            "ASSIGN a 10",
            "BEGIN",
            "INSERT b string",
            "ASSIGN b 'abc'",
            "BEGIN",
            "ASSIGN a 15",
            "INSERT a string",  
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "success", "success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = [
            "BEGIN",
            "BEGIN",
        ]
        expected = ["UnclosedBlock: 2"]
        
        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
        ]
        expected = ["UnclosedBlock: 2"]
        
        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = [
            "INSERT x number",
            "ASSIGN x y"
        ]
        expected = ["Undeclared: ASSIGN x y"]
        
        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = [
            "END",
            "END",
        ]
        expected = ["UnknownBlock"]
        
        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_23(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "END",
            "LOOKUP x",
        ]
        expected = ["Undeclared: LOOKUP x"]
        
        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_24(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "ASSIGN x 'aa'"
        ]
        expected = ["TypeMismatch: ASSIGN x 'aa'"]
        
        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_25(self):
        input = [
            "",
            "INSERT y string",
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_26(self):
        input = [
            "END 2",
        ]
        expected = ["Invalid: END 2"]
        
        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = [
            "INSERT x number",      
            "ASSIGN x x"  
        ]
        expected = ["success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 127))

    def test_28(self):
        input = [
            ""
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = [
            "ASSIGNNN x 10",
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = [
            "INSERT\ta\tnumber",
            "INSERT\tb\tstring",
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = [
            "INSERT str string",
            "ASSIGN str 'abc cd'",
        ]
        expected = ["Invalid: ASSIGN str 'abc cd'"]
        
        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = [
            "INSER 1x number",
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x"
        ]
        expected = ["Invalid: ASSIGN x"]
        
        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "ASSIGN x 42",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "x//0 y//1"]
        
        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "ASSIGN x 'hello'",
            "END",
        ]
        expected = ["success", "success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "ASSIGN x y",
            "END",
        ]
        expected = ["TypeMismatch: ASSIGN x y"]
        
        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "PRINT",
            "END",  
        ]
        expected = ["success", "success", "success", "x//0 y//1"]
        
        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "y//1 x//0"]
        
        self.assertTrue(TestUtils.check(input, expected, 138))

    def test_39(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "LOOKUP z",
            "END",
        ]
        expected = ["Undeclared: LOOKUP z"]
        
        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "ASSIGN z 42",
            "END",
        ]
        expected = ["Undeclared: ASSIGN z 42"]
        
        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "ASSIGN x 42",
            "END",
        ]
        expected = ["success", "success", "success", "success"]
        
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "ASSIGN x 42",
            "PRINT",
            "RPRINT",
            "LOOKUP x",
            "LOOKUP y",
            "LOOKUP z",
            "END",
        ]
        expected = ["Undeclared: LOOKUP z"]
        
        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "BEGIN",
            "INSERT z number",
            "ASSIGN z 100",
            "PRINT",
            "END",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "success", "x//0 y//1 z//2", "x//0 y//1"]
        
        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "INSERT y string",
            "ASSIGN x 'hcmut'",
            "BEGIN",
            "INSERT z number",
            "INSERT x number",
            "ASSIGN z x",
            "LOOKUP x",
            "END",
            "LOOKUP x",
            "END",
            "LOOKUP x",
        ]
        expected = ["success", "success", "success", "success", "success", "success", "success", "2", "1", "0"]
        
        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "BEGIN",
            "INSERT z number",
            "ASSIGN z 100",
            "LOOKUP z",
            "END",
            "LOOKUP z",
            "END",
        ]
        expected = ["Undeclared: LOOKUP z"]
        
        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = [

        ]
        expected = []
        
        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y 'hello'",
            "BEGIN",
            "INSERT z number",
            "ASSIGN z 100",
            "PRINT",
            "RPRINT",
            "LOOKUP x",
            "LOOKUP y",
            "LOOKUP z",
            "END",
            "PRINT",
            "RPRINT",
            "LOOKUP x",
            "LOOKUP y",
            "LOOKUP z",
            "END",
        ]
        expected = ["Undeclared: LOOKUP z"]
        
        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = [
            "INSERT o number",
            "INSERT hcmut string",
            " ASSIGN o 100",
            "ASSIGN hcmut 'hello'",
            "PRINT"
        ]
        expected = ["Invalid: Invalid command"]
        
        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = [
            "BEGIN",
            "PRINT",
        ]
        expected = ["UnclosedBlock: 1"]
        
        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_50(self):
        input = [
            "INSERT x number",
            "ASSIGN x 'byebye"
        ]
        expected = ["Invalid: ASSIGN x 'byebye"]
        
        self.assertTrue(TestUtils.check(input, expected, 150))