
from neo.Core.TX.Transaction import *
from neo.Fixed8 import Fixed8
import sys
from neo.Core.Blockchain import Blockchain

from autologging import logged

@logged
class ClaimTransaction(Transaction):

    Claims = set()


    @property
    def Size(self):
        return super(ClaimTransaction,self).Size() + sys.getsizeof(self.Claims)


    def __init__(self, *args, **kwargs):

        super(ClaimTransaction, self).__init__(*args, **kwargs)

        self.Type = TransactionType.ClaimTransaction



    def DeserializeExclusiveData(self, reader):

        self.Type = TransactionType.ClaimTransaction
        if self.Version != 0:
            raise Exception('Format Exception')


        numrefs = reader.ReadVarInt()

        claims = []
        for i in range(0, numrefs):
            c = CoinReference()
            c.Deserialize(reader)
            claims.append(c)

        self.Claims = claims
        if len(self.Claims) == 0:
            raise Exception('Format Exception')

    def GetScriptHashesForVerifying(self):

        raise NotImplementedError()

    def SerializeExclusiveData(self, writer):

        writer.WriteSerializableArray(self.Claims)


    def ToJson(self):

        json = super(ClaimTransaction,self).ToJson()

        json['claims'] = [claim.ToJson() for claim in self.Claims]

        return json

    def Verify(self, mempool):

        if not super(ClaimTransaction, self).Verify(mempool): return False

        #wat does this do
        #get all claim transactinos from mempool list
        #that are not this claim
        #and gather all the claims of those claim transactions
        #and see if they intersect the claims of this transaction
        #and if that number is greater than zero that we do not verify
        #(now, to do that in python)
        #if (mempool.OfType < ClaimTransaction > ().Where(p => p != this).SelectMany(p= > p.Claims).Intersect(Claims).Count() > 0)
        #return false;

        #im sorry about the below
        otherclaimTxs = [tx for tx in mempool if tx is ClaimTransaction and tx is not self]
        for other in otherclaimTxs:
            #check to see if the length of the intersection between this objects claim's and the other txs claims is > 0
            if len( [list(filter(lambda x: x in self.Claims, otherClaims)) for otherClaims in other.Claims ]): return False


        txResult = None
        for tx in self.GetTransactionResults():
            if tx.AssetId == Blockchain.SystemCoin().Hash:
                txResult = tx
                break

        if txResult is None or txResult.Amount > Fixed8(0): return False

        try:
            return Blockchain.CalculateBonusIgnoreClaimed(self.Claims,False) == -txResult.Amount

        except Exception as e:
            self.__log.debug('couldnt calculate bonus: %s ' % e)

        return False




