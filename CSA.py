
from math import sqrt

class CSA(object):
    def __init__(self,**kwargs):
        for key,val in kwargs.items():
            setattr(self, key, val)
        self.MtM_diff = None  # placeholder, ApplyThres is currently not used anywhere

    def ApplyThres(self,MtM_vector):
        MtM_len = len(MtM_vector)
        coll_MtM    = [0]*MtM_len
        collateral  = [0]*MtM_len/2
        coll_MtM[1] = MtM_vector[1]

        for i in range(1,MtM_len/2-1):
            if (coll_MtM[2*(i-1)+1]>self.thres_cpty+self.MTA_cpty):
                collateral[i] = coll_MtM[2*(i-1)+1]-self.thres_cpty-self.MTA_cpty
            elif (coll_MtM[2*(i-1)+1]< (-self.thres_cpty-self.MTA_cpty)):
                collateral[i] = coll_MtM[2*(i-1)+1]-self.thres_cpty-self.MTA_cpty
            elif (i>2 and collateral[i-1]>0 and self.MtM_diff<0):
                collateral[i] = max(collateral[i-1]-self.MtM_diff,0)
            elif (i>2 and collateral[i-1]<0 and self.MtM_diff>0):
                collateral[i] = min(collateral[i-1]+self.MtM_diff,0)
            elif (i>2):
                 collateral[i] = collateral[i-1]

            coll_MtM[2*i] = coll_MtM[2*i] - collateral[i]
            coll_MtM[2*i+1] = coll_MtM[2*i+1] - collateral[i]
        return coll_MtM

    def CalcMF(self):
          MPOR = 10 + self.remargin_freq -1
          return(1.5*sqrt(MPOR/250))
