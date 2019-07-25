import unittest
import time

import pyrplidar_protocol
from pyrplidar_protocol import *


class PyRPlidarProtocolTest(unittest.TestCase):

    def test_stop_req_packet(self):
        cmd = PyRPlidarCommand(RPLIDAR_CMD_STOP)
        self.assertEqual(cmd.raw_bytes, b"\xA5\x25")

    def test_reset_req_packet(self):
        cmd = PyRPlidarCommand(RPLIDAR_CMD_RESET)
        self.assertEqual(cmd.raw_bytes, b"\xA5\x40")

    def test_get_info_req_packet(self):
        cmd = PyRPlidarCommand(RPLIDAR_CMD_GET_INFO)
        self.assertEqual(cmd.raw_bytes, b"\xA5\x50")

    def test_parse_descriptor_01(self):
        descriptor = PyRPlidarResponse(b"\xA5\x5A\x04\x00\x00\x00\x15")
        self.assertEqual(descriptor.data_length, 0x04)
        self.assertEqual(descriptor.send_mode, 0)
        self.assertEqual(descriptor.data_type, 0x15)

    def test_parse_descriptor_02(self):
        descriptor = PyRPlidarResponse(b"\xA5\x5A\x84\x00\x00\x40\x84")
        self.assertEqual(descriptor.data_length, 0x84)
        self.assertEqual(descriptor.send_mode, 1)
        self.assertEqual(descriptor.data_type, 0x84)

    
    def test_varbitscale_decode(self):

        dist_major_input = [0x1E0, 0x20B, 0x219, 0x504, 0x507, 0x51E]
        dist_major_output = [0x1E0, 0x216, 0x232, 0x810, 0x81C, 0x878]
        scalelvl_output = [0, 1, 1 ,2, 2, 2]
    
        for i in range(len(dist_major_input)):
            dist_major, scalelvl = pyrplidar_protocol._varbitscale_decode(dist_major_input[i])
            self.assertEqual(dist_major, dist_major_output[i])
            self.assertEqual(scalelvl, scalelvl_output[i])
    
    
    def test_capsule_parsing(self):
        
        nodes_result = [
            [[0x2, 0xBC, 0xE282, 0x97C], [0x2, 0xBC, 0xE2EE, 0x970], [0x2, 0xBC, 0xE32D, 0x964], [0x2, 0xBC, 0xE3B0, 0x958], [0x2, 0xBC, 0xE3F1, 0x964], [0x2, 0xBC, 0xE45D, 0x96C], [0x2, 0xBC, 0xE4B3, 0x960], [0x2, 0xBC, 0xE4DB, 0x960], [0x2, 0xBC, 0xE549, 0x95C], [0x2, 0xBC, 0xE59F, 0x958], [0x2, 0xBC, 0xE60B, 0x94C], [0x2, 0xBC, 0xE64C, 0x958], [0x2, 0xBC, 0xE6A2, 0x960], [0x2, 0xBC, 0xE70E, 0x954], [0x2, 0xBC, 0xE763, 0x954], [0x2, 0xBC, 0xE7A4, 0x94C], [0x2, 0xBC, 0xE7FA, 0x93C], [0x2, 0xBC, 0xE84F, 0x938], [0x2, 0xBC, 0xE8A7, 0x938], [0x2, 0xBC, 0xE913, 0x938], [0x2, 0xBC, 0xE969, 0x934], [0x2, 0xBC, 0xE9BE, 0x934], [0x2, 0xBC, 0xE9E9, 0x934], [0x2, 0xBC, 0xEA55, 0x934], [0x2, 0xBC, 0xEAC1, 0x934], [0x2, 0xBC, 0xEB02, 0x938], [0x2, 0xBC, 0xEB58, 0x938], [0x2, 0xBC, 0xEBC4, 0x940], [0x2, 0xBC, 0xEC19, 0x94C], [0x2, 0xBC, 0xEC44, 0x948], [0x2, 0xBC, 0xECB0, 0x954], [0x2, 0xBC, 0xED05, 0x968]],
            [[0x2, 0xBC, 0xED47, 0x968], [0x2, 0xBC, 0xED99, 0x970], [0x2, 0xBC, 0xEE05, 0x974], [0x2, 0xBC, 0xEE58, 0x968], [0x2, 0xBC, 0xEE96, 0x964], [0x2, 0xBC, 0xEF19, 0x960], [0x2, 0xBC, 0xEF55, 0x958], [0x2, 0xBC, 0xEFC1, 0x958], [0x2, 0xBC, 0xF016, 0x95C], [0x2, 0xBC, 0xF03B, 0x96C], [0x2, 0xBC, 0xF091, 0x978], [0x2, 0xBC, 0xF0E3, 0x97C], [0x2, 0xBC, 0xF14F, 0x980], [0x2, 0xBC, 0xF1A4, 0x988], [0x2, 0xBC, 0xF1E0, 0x98C], [0x2, 0xBC, 0xF24C, 0x998], [0x2, 0xBC, 0xF28B, 0x9A0], [0x2, 0xBC, 0xF2DD, 0x9AC], [0x2, 0xBC, 0xF333, 0x9B0], [0x2, 0xBC, 0xF385, 0x9AC], [0x2, 0xBC, 0xF3DB, 0x9B0], [0x2, 0xBC, 0xF430, 0x9B4], [0x2, 0xBC, 0xF482, 0x9B8], [0x2, 0xBC, 0xF4C1, 0x9BC], [0x2, 0xBC, 0xF52D, 0x9C4], [0x2, 0xBC, 0xF569, 0x9C8], [0x2, 0xBC, 0xF5BE, 0x9D0], [0x2, 0xBC, 0xF627, 0x9D0], [0x2, 0xBC, 0xF666, 0x9D4], [0x2, 0xBC, 0xF6E9, 0x9DC], [0x2, 0xBC, 0xF724, 0x9E8], [0x2, 0xBC, 0xF77A, 0x9F4]],
            [[0x2, 0xBC, 0xF7CF, 0x9F4], [0x2, 0xBC, 0xF80B, 0xA04], [0x2, 0xBC, 0xF860, 0xA1C], [0x2, 0xBC, 0xF8B3, 0xA24], [0x2, 0xBC, 0xF908, 0xA2C], [0x2, 0xBC, 0xF95D, 0xA30], [0x2, 0xBC, 0xF9B0, 0xA30], [0x2, 0xBC, 0xFA05, 0xA34], [0x2, 0xBC, 0xFA71, 0xA38], [0x2, 0xBC, 0xFAC4, 0xA40], [0x2, 0xBC, 0xFB02, 0xA4C], [0x2, 0xBC, 0xFB6C, 0xA54], [0x1, 0xBC, 0xFBAA, 0xA5C], [0x2, 0xBC, 0xFC00, 0xA68], [0x2, 0xBC, 0xFC52, 0xA78], [0x2, 0xBC, 0xFC91, 0xA80], [0x2, 0xBC, 0xFCE6, 0xA90], [0x2, 0xBC, 0xFD4F, 0xA9C], [0x2, 0xBC, 0xFDA4, 0xA9C], [0x2, 0xBC, 0xFDF7, 0xAA0], [0x2, 0xBC, 0xFE36, 0xAA4], [0x2, 0xBC, 0xFEA2, 0xAA4], [0x2, 0xBC, 0xFEF4, 0xA9C], [0x2, 0xBC, 0xFF49, 0xA98], [0x2, 0xBC, 0xFF88, 0xA94], [0x2, 0xBC, 0xFFF1, 0xA94], [0x2, 0xBC, 0x30, 0xA98], [0x2, 0xBC, 0x82, 0xAA0], [0x2, 0xBC, 0xD8, 0xAAC], [0x2, 0xBC, 0x12D, 0xAB4], [0x2, 0xBC, 0x196, 0xAC0], [0x2, 0xBC, 0x1D5, 0xACC]],
            [[0x2, 0xBC, 0x22A, 0xAD4], [0x2, 0xBC, 0x27D, 0xADC], [0x2, 0xBC, 0x2E9, 0xAF0], [0x2, 0xBC, 0x324, 0xAF4], [0x2, 0xBC, 0x37A, 0xAE0], [0x2, 0xBC, 0x3E6, 0xAE4], [0x2, 0xBC, 0x438, 0xAE4], [0x2, 0xBC, 0x477, 0xAF0], [0x2, 0x0, 0x4E3, 0x0], [0x2, 0xBC, 0x536, 0xA88], [0x2, 0xBC, 0x58B, 0xA64], [0x2, 0xBC, 0x5C7, 0xA64], [0x2, 0xBC, 0x633, 0xA64], [0x2, 0xBC, 0x688, 0xA60], [0x2, 0xBC, 0x6DB, 0xA60], [0x2, 0x0, 0x730, 0x0], [0x2, 0xBC, 0x785, 0x9E8], [0x2, 0xBC, 0x7D8, 0xA24], [0x2, 0x0, 0xC5B, 0x0], [0x2, 0x0, 0xCAD, 0x0], [0x2, 0x0, 0x8BE, 0x0], [0x2, 0xBC, 0x913, 0xAEC], [0x2, 0xBC, 0x94F, 0xAF0], [0x2, 0xBC, 0x9BB, 0xAF4], [0x2, 0xBC, 0x9FA, 0xAFC], [0x2, 0xBC, 0xA63, 0xB04], [0x2, 0xBC, 0xAB8, 0xB14], [0x2, 0xBC, 0xB0B, 0xB28], [0x2, 0xBC, 0xB60, 0xB44], [0x2, 0xBC, 0xB9F, 0xB64], [0x2, 0xBC, 0xBF1, 0xB80], [0x2, 0xBC, 0xC30, 0xBB8]]]
                        
        data = [b"\xAC\x50\x12\x51\x7E\x09\x72\x09\xDE\x66\x09\x5A\x09\xCE\x66\x09\x6E\x09\xCD\x62\x09\x62\x09\xEC\x5E\x09\x5A\x09\xDD\x4E\x09\x5A\x09\xDC\x62\x09\x56\x09\xCD\x56\x09\x4E\x09\xDC\x3E\x09\x3A\x09\xDD\x3A\x09\x3A\x09\xCD\x36\x09\x36\x09\xCC\x36\x09\x36\x09\xDE\x36\x09\x3A\x09\xDC\x3A\x09\x42\x09\xCD\x4E\x09\x4A\x09\xEC\x56\x09\x6A\x09\xDD", b"\xAE\x5A\xDB\x54\x6A\x09\x72\x09\xEE\x76\x09\x6A\x09\xDD\x66\x09\x62\x09\xCE\x5A\x09\x5A\x09\xCD\x5E\x09\x6E\x09\xEC\x7A\x09\x7E\x09\xEE\x82\x09\x8A\x09\xDD\x8E\x09\x9A\x09\xDE\xA2\x09\xAE\x09\xEE\xB2\x09\xAE\x09\xEE\xB2\x09\xB6\x09\xEE\xBA\x09\xBE\x09\xFE\xC6\x09\xCA\x09\xFE\xD2\x09\xD2\x09\xEF\xD6\x09\xDE\x09\xDF\xEA\x09\xF6\x09\xEE", b"\xAE\x5B\x8F\x58\xF6\x09\x06\x0A\xFE\x1E\x0A\x26\x0A\xFF\x2E\x0A\x32\x0A\xFF\x32\x0A\x36\x0A\xFF\x3A\x0A\x42\x0A\xEE\x4E\x0A\x56\x0A\xEF\x5E\x0A\x6A\x0A\xFF\x7A\x0A\x83\x0A\x0F\x93\x0A\x9E\x0A\xF0\x9E\x0A\xA2\x0A\xFF\xA7\x0A\xA6\x0A\xF0\x9E\x0A\x9A\x0A\xFF\x97\x0A\x96\x0A\xF0\x9B\x0A\xA3\x0A\x00\xAF\x0A\xB7\x0A\x00\xC2\x0A\xCF\x0A\x0F", b"\xAF\x58\x43\x02\xD7\x0A\xDF\x0A\x00\xF2\x0A\xF7\x0A\x0F\xE3\x0A\xE6\x0A\xF0\xE6\x0A\xF3\x0A\x0F\x02\x00\x8A\x0A\xFF\x66\x0A\x67\x0A\x0F\x66\x0A\x62\x0A\xFF\x62\x0A\x02\x00\xFF\xEA\x09\x26\x0A\xFF\x00\x00\x00\x00\x00\x03\x00\xEF\x0A\x00\xF3\x0A\xF7\x0A\x01\xFF\x0A\x07\x0B\x01\x17\x0B\x2B\x0B\x00\x47\x0B\x67\x0B\x10\x83\x0B\xBB\x0B\x21", b"\xAB\x51\xF7\x05\x00\x00\x00\x00\x00\x03\x00\xD7\x0D\x33\x03\x0E\x13\x0E\x44\xFB\x0D\xC7\x0D\x33\x7B\x0D\x03\x00\x33\xC7\x0C\x8F\x0C\x23\x73\x0C\x67\x0C\x22\x5B\x0C\x5B\x0C\x21\x63\x0C\x6B\x0C\x21\x77\x0C\x8B\x0C\x22\xB3\x0C\xD3\x0C\x33\xEF\x0C\x17\x0D\x32\x53\x0D\x03\x00\x44\x27\x0E\x4B\x0E\x44\x53\x0E\x5B\x0E\x44\x5F\x0E\x6B\x0E\x44"]
        
        
        capsule_prev = PyRPlidarScanCapsule(data[0])
        capsule_current = None
        
        for i in range(1,5):
            capsule_current = PyRPlidarScanCapsule(data[i])
            
            nodes = pyrplidar_protocol._capsuleToNormal(capsule_prev, capsule_current)
            
            for j in range(len(nodes)):
                start_flag, quality, angle_z_q14, dist_mm_q2 = nodes_result[i-1][j]
                self.assertEqual(start_flag, nodes[j].start_flag)
                self.assertEqual(quality, nodes[j].quality)
                self.assertEqual(angle_z_q14, nodes[j].angle_z_q14)
                self.assertEqual(dist_mm_q2, nodes[j].dist_mm_q2)
            
            capsule_prev = capsule_current

    
    
    def test_dense_capsule_parsing(self):
        pass
    
    
    def test_ultra_capsule_parsing(self):
        
        nodes_result = [
            [[0x2, 0xBC, 0x331F, 0x454], [0x2, 0xBC, 0x3363, 0x458], [0x2, 0xBC, 0x33AA, 0x458], [0x2, 0xBC, 0x33EE, 0x458], [0x2, 0xBC, 0x3436, 0x458], [0x2, 0xBC, 0x347A, 0x454], [0x2, 0xBC, 0x34C1, 0x454], [0x2, 0xBC, 0x3505, 0x454], [0x2, 0xBC, 0x3549, 0x454], [0x2, 0xBC, 0x3591, 0x454], [0x2, 0xBC, 0x35D5, 0x454], [0x2, 0xBC, 0x361C, 0x454], [0x2, 0xBC, 0x3660, 0x454], [0x2, 0xBC, 0x36A7, 0x454], [0x2, 0xBC, 0x36EC, 0x454], [0x2, 0xBC, 0x373B, 0x450], [0x2, 0xBC, 0x378B, 0x444], [0x2, 0xBC, 0x37DB, 0x430], [0x2, 0xBC, 0x3836, 0x41C], [0x2, 0x0, 0x3522, 0x0], [0x2, 0x0, 0x3566, 0x0], [0x2, 0xBC, 0x3911, 0x40C], [0x2, 0x0, 0x35F1, 0x0], [0x2, 0x0, 0x3636, 0x0], [0x2, 0xBC, 0x3947, 0x4D0], [0x2, 0xBC, 0x3996, 0x4C4], [0x2, 0xBC, 0x39E6, 0x4B0], [0x2, 0xBC, 0x3A36, 0x4A8], [0x2, 0xBC, 0x3A7A, 0x4A4], [0x2, 0xBC, 0x3AC1, 0x4A4], [0x2, 0xBC, 0x3B05, 0x4A4], [0x2, 0xBC, 0x3B4C, 0x4A4], [0x2, 0xBC, 0x3B9C, 0x49C], [0x2, 0xBC, 0x3BE0, 0x49C], [0x2, 0xBC, 0x3C27, 0x49C], [0x2, 0xBC, 0x3C6C, 0x498], [0x2, 0xBC, 0x3CB0, 0x498], [0x2, 0xBC, 0x3CF7, 0x498], [0x2, 0xBC, 0x3D3B, 0x498], [0x2, 0xBC, 0x3D82, 0x498], [0x2, 0xBC, 0x3DC7, 0x498], [0x2, 0xBC, 0x3E0E, 0x498], [0x2, 0xBC, 0x3E52, 0x498], [0x2, 0xBC, 0x3E96, 0x498], [0x2, 0xBC, 0x3EDD, 0x498], [0x2, 0xBC, 0x3F22, 0x498], [0x2, 0xBC, 0x3F69, 0x49C], [0x2, 0xBC, 0x3FAD, 0x4A0], [0x2, 0xBC, 0x3FE9, 0x4A4], [0x2, 0xBC, 0x402D, 0x4A8], [0x2, 0xBC, 0x4074, 0x4AC], [0x2, 0xBC, 0x40B0, 0x4B0], [0x2, 0xBC, 0x40F4, 0x4B4], [0x2, 0xBC, 0x4138, 0x4BC], [0x2, 0xBC, 0x4174, 0x4C8], [0x2, 0xBC, 0x41B0, 0x4D0], [0x2, 0xBC, 0x41F7, 0x4D4], [0x2, 0xBC, 0x423B, 0x4DC], [0x2, 0xBC, 0x4277, 0x4E0], [0x2, 0xBC, 0x42BB, 0x4E4], [0x2, 0xBC, 0x4302, 0x4E4], [0x2, 0xBC, 0x4347, 0x4E4], [0x2, 0xBC, 0x438E, 0x4E4], [0x2, 0xBC, 0x43D2, 0x4E4], [0x2, 0xBC, 0x4416, 0x4E8], [0x2, 0x0, 0x419C, 0x0], [0x2, 0xBC, 0x44A2, 0x4EC], [0x2, 0xBC, 0x4511, 0x4A4], [0x2, 0xBC, 0x4560, 0x4A0], [0x2, 0xBC, 0x45A4, 0x4A0], [0x2, 0xBC, 0x45E0, 0x4A4], [0x2, 0xBC, 0x4627, 0x4A8], [0x2, 0xBC, 0x4663, 0x4B0], [0x2, 0x0, 0x43C9, 0x0], [0x2, 0x0, 0x440E, 0x0], [0x2, 0xBC, 0x4733, 0x4BC], [0x2, 0xBC, 0x4763, 0x4D4], [0x2, 0xBC, 0x479F, 0x4EC], [0x2, 0xBC, 0x47DB, 0x4F8], [0x2, 0xBC, 0x4816, 0x500], [0x2, 0xBC, 0x485B, 0x504], [0x2, 0xBC, 0x489F, 0x500], [0x2, 0xBC, 0x48EE, 0x4FC], [0x2, 0xBC, 0x4936, 0x4FC], [0x2, 0xBC, 0x4971, 0x500], [0x2, 0xBC, 0x49B6, 0x500], [0x2, 0x0, 0x474F, 0x0], [0x2, 0xBC, 0x4A41, 0x504], [0x2, 0xBC, 0x4AA4, 0x4D8], [0x2, 0xBC, 0x4AEC, 0x4D0], [0x2, 0xBC, 0x4B3B, 0x4C4], [0x2, 0xBC, 0x4B8B, 0x4BC], [0x2, 0xBC, 0x4BCF, 0x4B8], [0x2, 0xBC, 0x4C1F, 0x4AC], [0x2, 0xBC, 0x4C66, 0x4A8], [0x2, 0xBC, 0x4CAA, 0x4A4]],
            [[0x2, 0xBC, 0x4CEE, 0x4A4], [0x2, 0xBC, 0x4D2A, 0x4B4], [0x2, 0xBC, 0x4D66, 0x4C8], [0x2, 0xBC, 0x4DAA, 0x4CC], [0x2, 0xBC, 0x4DE3, 0x4D4], [0x2, 0xBC, 0x4E27, 0x4D8], [0x2, 0xBC, 0x4E6C, 0x4DC], [0x2, 0xBC, 0x4EA7, 0x4E8], [0x2, 0xBC, 0x4EE0, 0x4F0], [0x2, 0xBC, 0x4F27, 0x4F8], [0x2, 0x0, 0x4CB6, 0x0], [0x2, 0x0, 0x4CFA, 0x0], [0x2, 0xBC, 0x4FE9, 0x500], [0x2, 0x0, 0x4D82, 0x0], [0x2, 0x0, 0x4DC7, 0x0], [0x2, 0xBC, 0x5085, 0x568], [0x2, 0xBC, 0x50BE, 0x570], [0x2, 0xBC, 0x5102, 0x57C], [0x2, 0xBC, 0x513E, 0x580], [0x2, 0xBC, 0x5182, 0x580], [0x2, 0xBC, 0x51C7, 0x584], [0x2, 0xBC, 0x520B, 0x588], [0x2, 0xBC, 0x5252, 0x58C], [0x2, 0xBC, 0x5296, 0x590], [0x2, 0xBC, 0x52CF, 0x594], [0x2, 0xBC, 0x5313, 0x598], [0x2, 0xBC, 0x5358, 0x5A0], [0x2, 0xBC, 0x5393, 0x5AC], [0x2, 0xBC, 0x53CC, 0x5C4], [0x2, 0xBC, 0x5408, 0x5D8], [0x2, 0xBC, 0x544C, 0x5E0], [0x2, 0xBC, 0x5491, 0x5E4], [0x2, 0xBC, 0x54CC, 0x5F4], [0x2, 0xBC, 0x5505, 0x608], [0x2, 0xBC, 0x5549, 0x618], [0x2, 0xBC, 0x5585, 0x624], [0x2, 0xBC, 0x55C9, 0x630], [0x2, 0xBC, 0x5605, 0x638], [0x2, 0xBC, 0x5649, 0x640], [0x2, 0xBC, 0x568E, 0x644], [0x2, 0xBC, 0x56D2, 0x64C], [0x2, 0xBC, 0x570E, 0x658], [0x2, 0xBC, 0x5752, 0x664], [0x2, 0xBC, 0x578B, 0x66C], [0x2, 0x0, 0x55D2, 0x0], [0x2, 0xBC, 0x5833, 0x628], [0x2, 0xBC, 0x5877, 0x620], [0x2, 0xBC, 0x58BE, 0x620], [0x2, 0xBC, 0x590B, 0x618], [0x2, 0xBC, 0x5947, 0x624], [0x2, 0xBC, 0x5980, 0x634], [0x2, 0xBC, 0x59CF, 0x630], [0x2, 0xBC, 0x5A13, 0x628], [0x2, 0xBC, 0x5A58, 0x624], [0x2, 0xBC, 0x5A9C, 0x624], [0x2, 0xBC, 0x5AE3, 0x624], [0x2, 0xBC, 0x5B27, 0x624], [0x2, 0xBC, 0x5B6C, 0x624], [0x2, 0xBC, 0x5BB0, 0x620], [0x2, 0xBC, 0x5BF4, 0x620], [0x2, 0xBC, 0x5C38, 0x620], [0x2, 0xBC, 0x5C7D, 0x620], [0x2, 0xBC, 0x5CC1, 0x624], [0x2, 0xBC, 0x5D08, 0x624], [0x2, 0xBC, 0x5D4C, 0x62C], [0x2, 0x0, 0x5B74, 0x0], [0x2, 0xBC, 0x5DC9, 0x634], [0x2, 0x0, 0x5BFD, 0x0], [0x2, 0x0, 0x5C41, 0x0], [0x2, 0xBC, 0x5E6E, 0x6B4], [0x2, 0xBC, 0x5EAA, 0x6C0], [0x2, 0xBC, 0x5EEE, 0x6D0], [0x2, 0xBC, 0x5F33, 0x6D8], [0x2, 0xBC, 0x5F6E, 0x6E0], [0x2, 0xBC, 0x5FB3, 0x6E8], [0x2, 0xBC, 0x5FF7, 0x6F0], [0x2, 0xBC, 0x603B, 0x6F4], [0x2, 0xBC, 0x6077, 0x700], [0x2, 0xBC, 0x60BB, 0x704], [0x2, 0xBC, 0x6100, 0x70C], [0x2, 0xBC, 0x6144, 0x710], [0x2, 0xBC, 0x6188, 0x710], [0x2, 0xBC, 0x61CC, 0x710], [0x2, 0xBC, 0x6211, 0x710], [0x2, 0xBC, 0x6255, 0x710], [0x2, 0xBC, 0x629C, 0x70C], [0x2, 0xBC, 0x62E0, 0x70C], [0x2, 0xBC, 0x6324, 0x70C], [0x2, 0xBC, 0x6369, 0x710], [0x2, 0xBC, 0x63AD, 0x714], [0x2, 0xBC, 0x63F1, 0x718], [0x2, 0xBC, 0x6436, 0x71C], [0x2, 0x0, 0x62B0, 0x0], [0x2, 0xBC, 0x64B6, 0x728], [0x2, 0x0, 0x6338, 0x0], [0x2, 0x0, 0x637D, 0x0]],
            [[0x2, 0x0, 0x63C4, 0x0], [0x2, 0x0, 0x6408, 0x0], [0x2, 0x0, 0x644C, 0x0], [0x2, 0x0, 0x6493, 0x0], [0x2, 0x0, 0x64D8, 0x0], [0x2, 0x0, 0x651F, 0x0], [0x2, 0x0, 0x6563, 0x0], [0x2, 0x0, 0x65A7, 0x0], [0x2, 0x0, 0x65EE, 0x0], [0x2, 0xBC, 0x6666, 0x1AA0], [0x2, 0xBC, 0x66AD, 0x1A60], [0x2, 0xBC, 0x66F1, 0x1A38], [0x2, 0xBC, 0x6736, 0x1A18], [0x2, 0xBC, 0x677D, 0x19F0], [0x2, 0xBC, 0x67C1, 0x19D0], [0x2, 0xBC, 0x6808, 0x19A8], [0x2, 0xBC, 0x6858, 0x1990], [0x2, 0xBC, 0x689C, 0x1980], [0x2, 0xBC, 0x68E0, 0x1958], [0x2, 0xBC, 0x6927, 0x1930], [0x2, 0xBC, 0x696C, 0x1900], [0x2, 0xBC, 0x69B3, 0x18D8], [0x2, 0xBC, 0x69F7, 0x18C0], [0x2, 0xBC, 0x6A3B, 0x18B0], [0x2, 0xBC, 0x6A82, 0x18A0], [0x2, 0xBC, 0x6AC7, 0x1888], [0x2, 0xBC, 0x6B0E, 0x1870], [0x2, 0xBC, 0x6B52, 0x1858], [0x2, 0xBC, 0x6B96, 0x1838], [0x2, 0xBC, 0x6BDD, 0x1818], [0x2, 0xBC, 0x6C2D, 0x17F8], [0x2, 0xBC, 0x6C71, 0x17E8], [0x2, 0xBC, 0x6CB6, 0x17D0], [0x2, 0xBC, 0x6CFD, 0x17B8], [0x2, 0xBC, 0x6D41, 0x17A0], [0x2, 0xBC, 0x6D88, 0x1790], [0x2, 0xBC, 0x6DCC, 0x1778], [0x2, 0xBC, 0x6E11, 0x1760], [0x2, 0xBC, 0x6E58, 0x1750], [0x2, 0xBC, 0x6E9C, 0x1728], [0x2, 0xBC, 0x6EE3, 0x1710], [0x2, 0xBC, 0x6F27, 0x1710], [0x2, 0xBC, 0x6F6C, 0x1700], [0x2, 0xBC, 0x6FB3, 0x16E0], [0x2, 0xBC, 0x6FF7, 0x16C8], [0x2, 0xBC, 0x703E, 0x16C0], [0x2, 0xBC, 0x7082, 0x16B0], [0x2, 0xBC, 0x70C7, 0x16A0], [0x2, 0xBC, 0x7116, 0x1690], [0x2, 0xBC, 0x715D, 0x1678], [0x2, 0xBC, 0x71A2, 0x1660], [0x2, 0xBC, 0x71E9, 0x1650], [0x2, 0xBC, 0x722D, 0x1640], [0x2, 0xBC, 0x7271, 0x1638], [0x2, 0xBC, 0x72B8, 0x1630], [0x2, 0xBC, 0x72FD, 0x1620], [0x2, 0xBC, 0x7344, 0x1610], [0x2, 0xBC, 0x7388, 0x1600], [0x2, 0xBC, 0x73CC, 0x15F0], [0x2, 0xBC, 0x7413, 0x15E0], [0x2, 0xBC, 0x7458, 0x15D0], [0x2, 0xBC, 0x749F, 0x15C0], [0x2, 0xBC, 0x74E3, 0x15B0], [0x2, 0xBC, 0x7527, 0x15A0], [0x2, 0xBC, 0x756E, 0x1598], [0x2, 0xBC, 0x75B3, 0x1588], [0x2, 0xBC, 0x75FA, 0x1580], [0x2, 0xBC, 0x763E, 0x1578], [0x2, 0xBC, 0x7682, 0x1570], [0x2, 0xBC, 0x76C9, 0x1568], [0x2, 0xBC, 0x770E, 0x1560], [0x2, 0xBC, 0x775D, 0x1550], [0x2, 0xBC, 0x77A2, 0x1550], [0x2, 0xBC, 0x77E9, 0x1548], [0x2, 0xBC, 0x782D, 0x1538], [0x2, 0xBC, 0x7874, 0x1528], [0x2, 0xBC, 0x78B8, 0x1520], [0x2, 0xBC, 0x78FD, 0x1518], [0x2, 0xBC, 0x7944, 0x1510], [0x2, 0xBC, 0x7988, 0x1508], [0x2, 0xBC, 0x79CF, 0x1500], [0x2, 0xBC, 0x7A13, 0x14F8], [0x2, 0xBC, 0x7A58, 0x14F8], [0x2, 0xBC, 0x7A9F, 0x14F0], [0x2, 0xBC, 0x7AE3, 0x14E8], [0x2, 0xBC, 0x7B2A, 0x14E0], [0x2, 0xBC, 0x7B6E, 0x14D8], [0x2, 0xBC, 0x7BB3, 0x14D0], [0x2, 0xBC, 0x7BFA, 0x14D8], [0x2, 0x0, 0x7BE3, 0x0], [0x2, 0xBC, 0x7C85, 0x14D0], [0x2, 0x0, 0x7C6E, 0x0], [0x2, 0xBC, 0x7E2D, 0x858], [0x2, 0xBC, 0x7E71, 0x848], [0x2, 0xBC, 0x7EB6, 0x840], [0x2, 0xBC, 0x7EFD, 0x838]],
            [[0x2, 0xBC, 0x7F41, 0x838], [0x2, 0xBC, 0x7F88, 0x838], [0x2, 0xBC, 0x7FCC, 0x838], [0x2, 0xBC, 0x8011, 0x840], [0x2, 0xBC, 0x8055, 0x840], [0x2, 0xBC, 0x809C, 0x850], [0x2, 0xBC, 0x80E0, 0x858], [0x2, 0x0, 0x7FAD, 0x0], [0x2, 0x0, 0x7FF1, 0x0], [0x2, 0x0, 0x8036, 0x0], [0x2, 0x0, 0x807D, 0x0], [0x2, 0x0, 0x80C1, 0x0], [0x2, 0x0, 0x8105, 0x0], [0x2, 0x0, 0x8149, 0x0], [0x2, 0x0, 0x8191, 0x0], [0x2, 0xBC, 0x8233, 0x1470], [0x2, 0xBC, 0x8277, 0x1490], [0x2, 0xBC, 0x82BB, 0x1490], [0x2, 0xBC, 0x8300, 0x1490], [0x2, 0xBC, 0x8347, 0x1490], [0x2, 0xBC, 0x838B, 0x1490], [0x2, 0xBC, 0x83CF, 0x1490], [0x2, 0xBC, 0x8416, 0x1490], [0x2, 0xBC, 0x845B, 0x1490], [0x2, 0xBC, 0x849F, 0x1498], [0x2, 0xBC, 0x84E6, 0x1498], [0x2, 0xBC, 0x852A, 0x14A0], [0x2, 0xBC, 0x856E, 0x14A8], [0x2, 0xBC, 0x85B3, 0x14A0], [0x2, 0xBC, 0x85FA, 0x14A0], [0x2, 0xBC, 0x863E, 0x14A0], [0x2, 0xBC, 0x8682, 0x14A8], [0x2, 0x0, 0x866C, 0x0], [0x2, 0xBC, 0x870E, 0x14B8], [0x2, 0xBC, 0x8766, 0x1330], [0x2, 0xBC, 0x87AD, 0x1320], [0x2, 0xBC, 0x87F1, 0x1320], [0x2, 0x0, 0x87C7, 0x0], [0x2, 0x0, 0x880B, 0x0], [0x2, 0xBC, 0x88C1, 0x1328], [0x2, 0xBC, 0x88F1, 0x14D0], [0x2, 0xBC, 0x8936, 0x14D8], [0x2, 0xBC, 0x897D, 0x14D8], [0x2, 0xBC, 0x89C1, 0x14E8], [0x2, 0xBC, 0x8A05, 0x14F0], [0x2, 0xBC, 0x8A4C, 0x14F8], [0x2, 0xBC, 0x8A91, 0x1500], [0x2, 0xBC, 0x8AD5, 0x1500], [0x2, 0xBC, 0x8B19, 0x1508], [0x2, 0xBC, 0x8B60, 0x1510], [0x2, 0xBC, 0x8BA4, 0x1518], [0x2, 0xBC, 0x8BE9, 0x1520], [0x2, 0xBC, 0x8C30, 0x1528], [0x2, 0xBC, 0x8C74, 0x1530], [0x2, 0xBC, 0x8CB8, 0x1538], [0x2, 0xBC, 0x8D00, 0x1550], [0x2, 0x0, 0x8CE6, 0x0], [0x2, 0xBC, 0x8E88, 0x8C0], [0x2, 0xBC, 0x8ED8, 0x8B0], [0x2, 0xBC, 0x8F1C, 0x8A8], [0x2, 0xBC, 0x8F60, 0x8A8], [0x2, 0xBC, 0x8FA7, 0x8A0], [0x2, 0xBC, 0x8FEC, 0x8A0], [0x2, 0xBC, 0x9030, 0x8A8], [0x2, 0xBC, 0x9074, 0x8A8], [0x2, 0xBC, 0x90BB, 0x8B0], [0x2, 0xBC, 0x90F4, 0x8C0], [0x2, 0x0, 0x8FE0, 0x0], [0x2, 0x0, 0x9024, 0x0], [0x2, 0x0, 0x9069, 0x0], [0x2, 0x0, 0x90B0, 0x0], [0x2, 0x0, 0x90F4, 0x0], [0x2, 0x0, 0x9138, 0x0], [0x2, 0x0, 0x9180, 0x0], [0x2, 0x0, 0x91C4, 0x0], [0x2, 0x0, 0x9208, 0x0], [0x2, 0x0, 0x924C, 0x0], [0x2, 0x0, 0x9293, 0x0], [0x2, 0x0, 0x92D8, 0x0], [0x2, 0x0, 0x931C, 0x0], [0x2, 0x0, 0x9363, 0x0], [0x2, 0xBC, 0x94CF, 0x9F0], [0x2, 0xBC, 0x9513, 0x9E8], [0x2, 0xBC, 0x955B, 0x9F0], [0x2, 0xBC, 0x959F, 0xA00], [0x2, 0xBC, 0x95E3, 0xA08], [0x2, 0xBC, 0x962A, 0xA08], [0x2, 0xBC, 0x966E, 0xA08], [0x2, 0xBC, 0x96B3, 0xA10], [0x2, 0xBC, 0x96F7, 0xA18], [0x2, 0xBC, 0x9733, 0xA20], [0x2, 0xBC, 0x9777, 0xA28], [0x2, 0xBC, 0x97BE, 0xA38], [0x2, 0xBC, 0x9802, 0xA38], [0x2, 0xBC, 0x9847, 0xA48], [0x2, 0xBC, 0x988E, 0xA50]]]
        
        
        data = [b"\xA0\x5B\xBE\x12\x15\x11\x00\x00\x16\x01\x00\x00\x15\x01\x00\x00\x15\x01\x00\x00\x15\x01\x40\x00\x14\xD1\x7F\x01\x07\xF1\xDF\x7F\x03\xF1\xDF\x7F\x34\xD1\xBF\x00\x2A\xF1\x3F\x00\x29\x01\x00\x00\x27\x01\x00\x00\x26\x01\x00\x00\x26\x01\x00\x00\x26\x01\x00\x00\x26\x11\xC0\xFF\x29\x11\xC0\xFF\x2C\x11\x40\xFF\x32\x21\x80\xFF\x37\x11\x00\x00\x39\x01\x00\x00\x39\x11\xC0\x7F\x3B\xE1\x3E\x00\x28\x11\x80\xFF\x2C\xF1\xDF\x7F\x2F\x61\x40\xFF\x3E\x21\x40\x00\x40\xF1\xFF\xFF\x40\x01\xC0\x7F\x41\x51\xFF\x00\x31\xE1\xFF\x00\x2B\xF1\x3F\x00", b"\xAC\x58\xE7\x1B\x29\x41\xC0\xFF\x33\x21\xC0\xFF\x37\x31\x80\xFF\x3E\xF1\xDF\x7F\x40\xF1\xDF\x7F\x5A\x21\xC0\xFF\x60\x01\xC0\xFF\x62\x11\xC0\xFF\x65\x11\x40\xFF\x6B\x61\x80\xFF\x78\x11\xC0\xFE\x82\x41\x40\xFF\x8C\x21\xC0\xFF\x91\x21\x40\xFF\x99\x21\xC0\x7F\x8A\xE1\xBF\x00\x86\x31\x40\x00\x8C\xE1\x3F\x00\x89\x01\x00\x00\x89\xF1\x3F\x00\x88\x01\x00\x00\x89\x21\xC0\x7F\x8D\xF1\xDF\x7F\xAD\x31\x80\xFF\xB6\x21\x80\xFF\xBC\x11\xC0\xFF\xC1\x21\x00\x00\xC4\x01\x00\x00\xC4\xF1\x3F\x00\xC3\x11\xC0\xFF\xC6\x11\xC0\x7F\xCA\xF1\xDF\x7F", b"\xAE\x54\xF3\x24\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x54\x84\x3F\x01\x43\xB4\x7F\x01\x35\xD4\x7F\x01\x2B\xB4\x7F\x01\x1B\xD4\xBF\x00\x14\xD4\xFF\x00\x0B\xC4\x3F\x01\xFF\xE3\xFF\x00\xF7\xD3\xFF\x00\xEF\xD3\x7F\x01\xE5\xD3\xBF\x00\xE0\xC3\x7F\x00\xD8\xE3\xBF\x00\xD2\xD3\xBF\x00\xCA\xE3\x7F\x00\xC6\xE3\xBF\x00\xC0\xE3\xBF\x00\xBA\xE3\xBF\x00\xB4\xF3\x7F\x00\xB0\xF3\x7F\x00\xAD\xF3\x3F\x00\xAA\xF3\xBF\x00\xA5\xF3\x7F\x00\xA2\xF3\x7F\x00\x9F\x03\x40\x00\x9D\xF3\x7F\x00\x9A\x13\xC0\x7F\x9A\xF3\x9F\x00\x09\xF2\x3F\x00", b"\xA3\x5A\x19\x2E\x07\x02\xC0\xFF\x08\x02\xC0\xFF\x0B\xF2\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x8E\x43\x00\x00\x92\x03\x00\x00\x92\x03\xC0\xFF\x93\x03\xC0\xFF\x95\xF3\x3F\x00\x94\x13\xC0\x7F\x97\xF3\x3C\x00\x64\xF3\xDF\x7F\x65\x53\x03\x00\x9B\x23\xC0\xFF\x9F\x13\xC0\xFF\xA1\x13\xC0\xFF\xA4\x13\xC0\xFF\xA7\x33\xC0\x7F\x18\xE2\x3F\x00\x15\xF2\xFF\xFF\x15\x02\x80\xFF\x18\xF2\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x3E\xF2\xBF\xFF\x40\x12\x00\x00\x41\x12\xC0\xFF\x44\x12\x00\x00\x47\x22\xC0\xFF", b"\xAC\x53\x36\x37\x4B\x12\x80\xFF\x4F\x12\x40\xFF\x55\x02\xC0\xFF\x56\x22\xC0\xFF\x5B\x12\xC0\xFF\x5F\x22\x80\xFF\x64\x12\xC0\x7F\x68\xF2\xDF\x7F\x00\xE0\xBF\xFF\x1F\x73\x40\x01\x22\x23\xC0\x7F\x5F\x63\xC0\x7F\x6D\xF3\xDF\x7F\x00\x50\xCF\x7F\x9B\xE2\x7F\x00\x98\x02\xC0\xFF\x9A\xF2\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x00\xF0\xDF\x7F\x00\x70\xC0\x00\x60\xE3\xFF\x7F\x5B\xF3\xDF\x7F\x00\xF0\xDF\x7F\x51\x53\xFF\x7F\x46\xF3\xDF\x7F\x00\xF0\x9F\x00\x34\xF3\xDF\x7F\x30\xF3\xDF\x7F\x00\x70\x80\x00\x22\xF3\xBF\x00\x1D\xE3\x7F\x00"]

        capsule_prev = PyRPlidarScanUltraCapsule(data[0])
        capsule_current = None
        
        for i in range(1,5):
            
            capsule_current = PyRPlidarScanUltraCapsule(data[i])
        
            nodes = pyrplidar_protocol._ultraCapsuleToNormal(capsule_prev, capsule_current)

            for j in range(len(nodes)):
                start_flag, quality, angle_z_q14, dist_mm_q2 = nodes_result[i-1][j]
                self.assertEqual(start_flag, nodes[j].start_flag)
                self.assertEqual(quality, nodes[j].quality)
                self.assertEqual(angle_z_q14, nodes[j].angle_z_q14)
                self.assertEqual(dist_mm_q2, nodes[j].dist_mm_q2)

            capsule_prev = capsule_current




if __name__ == "__main__":
    
    start_time = time.time()
    unittest.main()
    end_time = time.time()
    print("WorkingTime: {} sec".format(end_time-start_time))
