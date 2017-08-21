import unittest
import binascii

from neo.IO.Helper import Helper
from neo.Core.Blockchain import Blockchain
from neo.Core.TX.Transaction import TransactionType
from neo.Implementations.Blockchains.LevelDB.TestLevelDBBlockchain import TestLevelDBBlockchain
import json
class SmartContractTest(unittest.TestCase):
    LEVELDB_TESTPATH = './fixtures/TestSC'
    _blockchain = None


    @classmethod
    def setUpClass(self):
        self._blockchain = TestLevelDBBlockchain(path=self.LEVELDB_TESTPATH)
        Blockchain.RegisterBlockchain(self._blockchain)

    @classmethod
    def tearDownClass(self):
        self._blockchain.Dispose()

    def test_a_initial_setup(self):

        self.assertEqual(self._blockchain.Height, 2002)

    invb = b'00000000a94e2dacf44d6b4b1d2dd1929c6b77416201a2db8d0b762636b1098568159ab46d957d397ff13b229f4d122b70a0165ecadc6ef306bdc6b87e776613c42dd96912531359d3070000c6c7788f27c7322ef3812db982f3b0089a21a278988efeec6a027b2501fd450140eea7535f35ef9568f6e90bcac4c800e03f3c442670d2361bae5200ce26dca45f945735cb9363370ca31872ffc615d54dcf5833f72b1f82540d08162d0c1e936c4082b07301341f87e7a1b006698b39a1ca65829c26b02f405a4828359696b99c0ce91c6d3dcb4937f52d351373bb7208b42a92aad2df260c3c236a9e8f72465c1740b22665c229017775be08a2b874bb5e3acb4e8bedebbe328b18ee9f7c5e4842a17a801d6c4871e6c1740dbe77e72a1e29f49fd44a1a229802d6ad37512867714c40acd3f2543d1b15bd261f59f5d2011692981a3556e458e74d5855f4bb390ecc2f28c4874d21bdadecb9b25d5aec77d1acff4bce4a7e4633cf849230d7cb1b7cfa4085bdbc115dd0115d949b6b76bc74a2b6166f86d4f5b58ce38e11ea509291600973209d9f9718a336cd1c0e3ea9418643d39d3b216819cbd0f08393f643389575f155210209e7fd41dfb5c2f8dc72eb30358ac100ea8c72da18847befe06eade68cebfcb9210327da12b5c40200e9f65569476bbff2218da4f32548ff43b6387ec1416a231ee821034ff5ceeac41acf22cd5ed2da17a6df4dd8358fcb2bfb1a43208ad0feaab2746b21026ce35b29147ad09e4afe4ec4a7319095f08198fa8babbe3c56e970b143528d2221038dddc06ce687677a53d54f096d2591ba2302068cf123c1f2d75c2dddc542557921039dafd8571a641058ccc832c5e2111ea39b09c0bde36050914384f7a48bce9bf92102d02b1873a0863cd042cc717da31cea0d7cf9db32b74d4c72c01b0011503e2e2257ae020000c6c7788f00000000d100644011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111081234567890abcdef0415cd5b0769cc4ee2f1c9f4e0782756dabf246d0a4fe60a035400000000'
    invbh = b'0f72795fd62d5e7eeb65ce1452388343224cbc43cf56a0e8af866db07209a43c'
    invtxh = '4011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111081234567890abcdef0415cd5b0769cc4ee2f1c9f4e0782756dabf246d0a4fe60a0354'

    def test_a_invocation_block(self):

        hexdata = binascii.unhexlify(self.invb)

        block = Helper.AsSerializableWithType(hexdata, 'neo.Core.Block.Block')

        self.assertEqual(block.Hash.ToBytes(), self.invbh)
        self.assertEqual(block.Index, 2003)

        invtx = None
        for tx in block.Transactions:
            if tx.Type == TransactionType.InvocationTransaction:
                invtx = tx

        self.assertIsNotNone(invtx)


        self.assertEqual(len(invtx.Script), 100)
        self.assertEqual(invtx.Script.hex(), self.invtxh)


    def test_a_run_sc(self):

        hexdata = binascii.unhexlify(self.invb)

        block = Helper.AsSerializableWithType(hexdata, 'neo.Core.Block.Block')

        result = self._blockchain.Persist(block)

        self.assertTrue(result)


    asset_create_213686 = b'000000004cb2a38f901afb2b85869161bd96f930babdbf65bd04c4842fe625ecc1a7a725e99a7bc87264d857405ebe90b88bfa5b279da7a92a32b0a3771ac560f1d0cc82e6ff5559b6420300a8a6a761b68e326df3812db982f3b0089a21a278988efeec6a027b2501fd4501408e6ceb56b2a98213e0027245920faa279f48b14279874634edd0ad2f06fc80a785545f6419f4400822b3f5f270e76b39718764a1476d95a1349e4f8398220ddf4091718c9eed0bd2faa38b964198787816b067a4d7268251b6bf348732e6848a2fc88cd7b17b55610586226584202a754196a9b70fde3936d9854fbc3724ce5a8940e16d39bf14a1313ddbc681f01e346386e23308e39074bd01e77ed5dc9196e6b6aa9806bd904d1d0d171edf6c563e4ad99dd5adbd64021c8c5e4c48a6b3aaeb4140e6482ec6c1bb8e21ec28b55bbb6ee8b34ced411f71bb25452bb68666c834b4a9d2cc152440720f9efb0e701024143d4a8fea7c985918048600ac44da0823f09240a6441778043e226d3e34e4e54b3c89e237ae8517034d131d4efc42b8eeb8f2a8a8f4fad014728ff3bf34782c3328146cda7a89bdc29d045ad28786c02c2a5af9f155210209e7fd41dfb5c2f8dc72eb30358ac100ea8c72da18847befe06eade68cebfcb9210327da12b5c40200e9f65569476bbff2218da4f32548ff43b6387ec1416a231ee821034ff5ceeac41acf22cd5ed2da17a6df4dd8358fcb2bfb1a43208ad0feaab2746b21026ce35b29147ad09e4afe4ec4a7319095f08198fa8babbe3c56e970b143528d2221038dddc06ce687677a53d54f096d2591ba2302068cf123c1f2d75c2dddc542557921039dafd8571a641058ccc832c5e2111ea39b09c0bde36050914384f7a48bce9bf92102d02b1873a0863cd042cc717da31cea0d7cf9db32b74d4c72c01b0011503e2e2257ae020000a8a6a76100000000d1019b1467f97110a66136d38badc7b9f88eab013027ce491467f97110a66136d38badc7b9f88eab013027ce4921034b44ed9c8a88fb2497b6b57206cc08edd42c5614bd1fee790e5b795dee0f4e11520500e40b54022d5b7b226c616e67223a227a682d434e222c226e616d65223a22476c6f62616c4173736574546573743032227d5d01606816416e745368617265732e41737365742e43726561746500beb72e74000000012067f97110a66136d38badc7b9f88eab013027ce49011421b58d4586c06887514f7e272b0851d83e3e7d99727a6cb2c738ffc25300d0000001e72d286979ee6cb1b7e65dfddfb2e384100b8d148e7758de42e4168b71792c6000d63d0e2c2f000067f97110a66136d38badc7b9f88eab013027ce490141403a06a71d5398b13adf03aa61f21820d48eca9ff312482284089504881995f606ec400da3fb36d9a307e44beb05b083c590a55b17272d0ca82d861d484063ef392321034b44ed9c8a88fb2497b6b57206cc08edd42c5614bd1fee790e5b795dee0f4e11ac'


    def test_b_initial_setup(self):

        hexdata = binascii.unhexlify(self.asset_create_213686)

#        block = Helper.AsSerializableWithType(hexdata, 'neo.Core.Block.Block')

#        tx = block.Transactions
#        invtx = block.Transactions[1]
#        print("inv tx %s " % invtx)

#        self.assertEqual(invtx.Type, TransactionType.InvocationTransaction)


#        result = self._blockchain.Persist(block)
