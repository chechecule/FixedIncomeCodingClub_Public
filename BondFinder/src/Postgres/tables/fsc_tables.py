"""
Table creation strings all kept here so that it can by easily managed.
"""


fsc_bond_issue = """
    CREATE TABLE fsc_bond_issue
        (
            basDt date, crno text, isinCd text, ininCdNm text, scrsItmsKcd text,
            scrsItmsKcdNm text, bondIssuCurCd text, bondIssuCurCdNm text,
            bondIsurNm text, sicNm text, bondIssuDt text, bondExprDt text,
            irtChngDcd text, irtChngDcdNm text, bondSrfcInrt text, grnDcd text,
            grnDcdNm text, bondRnknDcd text, bondRnknDcdNm text, optnTcd text,
            optnTcdNm text, pclrBondKcd text, pclrBondKcdNm text, bondIssuAmt text,
            bondPymtAmt text, bondBal text, bondOffrMcd text, bondOffrMcdNm text,
            lstgDt text, txtnDcd text, txtnDcdNm text, pamtRdptMcd text, pamtRdptMcdNm text,
            stripsPsblYn text, stripsNm text, prisLnkgBondYn text, piamPayInstNm text,
            piamPayBrofNm text, cptUsgeDcd text, cptUsgeDcdNm text, bondRegInstDcd text,
            bondRegInstDcdNm text, issuDptyNm text, bondUndtInstNm text, bondGrnInstNm text,
            cpbdMngCmpyNm text, crfndYn text, prmncBondYn text, qibTrgtScrtYn text,
            prmncBondTmnDt text, rgtExertMnbdDcd text, rgtExertMnbdDcdNm text, intCmpuMcd text,
            intCmpuMcdNm text, qibTmnDt text, bondIntTcd text, bondIntTcdNm text,
            intPayCyclCtt text,  nxtmCopnDt text, rbfCopnDt text, bnkHldyIntPydyDcd text,
            bnkHldyIntPydyDcdNm text, sttrHldyIntPydyDcd text, sttrHldyIntPydyDcdNm text,
            intPayMmntDcd text, intPayMmntDcdNm text, elpsIntPayYn text, kisScrsItmsKcd text,
            kisScrsItmsKcdNm text, kbpScrsItmsKcd text, kbpScrsItmsKcdNm text,
            niceScrsItmsKcd text, niceScrsItmsKcdNm text, fnScrsItmsKcd text, fnScrsItmsKcdNm text,
            UNIQUE (basDt, isinCd)
        )

"""
