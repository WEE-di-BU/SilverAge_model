import math

# Model A
def type2_female_raw_a(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_gestdiab, b_learning, b_manicschiz, b_pos, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.986227273941040]

    Iethrisk = [
        0,
        0,
        1.0695857881565456,
        1.3430172097414006,
        1.8029022579794518,
        1.127465451770802,
        0.421463149023991,
        0.2850919645908353,
        0.8815108797589199,
        0.3660573343168487
    ]
    Ismoke = [
        0,
        0.06560169017505906,
        0.28450988673698374,
        0.3567664381700702,
        0.5359517110678775
    ]

    dage = age / 10
    age_2 = dage ** 3
    age_1 = dage ** 0.5
    dbmi = bmi / 10
    bmi_1 = dbmi
    bmi_2 = dbmi ** 3

    age_1 -= 2.123332023620606
    age_2 -= 91.64474487304688
    bmi_1 -= 2.571253299713135
    bmi_2 -= 16.999439239501953
    town -= 0.391116052865982

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 4.340085269913928
    a += age_2 * -0.004877170269615888
    a += bmi_1 * 2.9320361259524925
    a += bmi_2 * -0.04740020587484349
    a += town * 0.03734056961804915

    a += b_atypicalantipsy * 0.5526764611098438
    a += b_corticosteroids * 0.267922336806746
    a += b_cvd * 0.1779722905458669
    a += b_gestdiab * 1.5248871531467574
    a += b_learning * 0.2783514358717272
    a += b_manicschiz * 0.2618085210917906
    a += b_pos * 0.3406173988206666
    a += b_statin * 0.6590728773280822
    a += b_treatedhyp * 0.4394758285813712
    a += fh_diab * 0.5313359456558734

    a += age_1 * b_atypicalantipsy * -0.8031518398316395
    a += age_1 * b_learning * -0.8641596002882057
    a += age_1 * b_statin * -1.9757776696583935
    a += age_1 * bmi_1 * 0.6553138757562945
    a += age_1 * bmi_2 * -0.03620965720163018
    a += age_1 * fh_diab * -0.2641171450558896
    a += age_2 * b_atypicalantipsy * 0.000468404118102105
    a += age_2 * b_learning * 0.000672496880895336
    a += age_2 * b_statin * 0.0023750534194347966
    a += age_2 * bmi_1 * -0.004471966244526305
    a += age_2 * bmi_2 * 0.0001185479967753342
    a += age_2 * fh_diab * 0.0004161025828904768

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score

# Model B
def type2_female_raw_b(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_gestdiab, b_learning, b_manicschiz, b_pos, b_statin, b_treatedhyp, bmi, ethrisk, fbs, fh_diab, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.990905702114105]

    Iethrisk = [
        0,
        0,
        0.9898906127239111,
        1.2511504196326508,
        1.493475756819612,
        0.9673887434565966,
        0.4844644519593178,
        0.4784214955360103,
        0.7520946270805577,
        0.4050880741541424
    ]
    Ismoke = [
        0,
        0.03741563072369632,
        0.2252973672514483,
        0.3099736428023663,
        0.4361942139496418
    ]

    dage = age / 10
    age_1 = dage ** 0.5
    age_2 = dage ** 3
    dbmi = bmi / 10
    bmi_2 = dbmi ** 3
    bmi_1 = dbmi
    dfbs = fbs
    fbs_2 = (dfbs ** -1) * math.log(dfbs)
    fbs_1 = dfbs ** -1

    age_1 -= 2.123332023620606
    age_2 -= 91.64474487304688
    bmi_1 -= 2.571253299713135
    bmi_2 -= 16.999439239501953
    fbs_1 -= 0.20830936729908
    fbs_2 -= 0.326781362295151
    town -= 0.391116052865982

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 3.765012950751728
    a += age_2 * -0.005604334343661494
    a += bmi_1 * 2.4410935031672469
    a += bmi_2 * -0.04215263347990964
    a += fbs_1 * -2.1887891946337308
    a += fbs_2 * -69.96084198286603
    a += town * 0.03580462976631265

    a += b_atypicalantipsy * 0.4748378550253853
    a += b_corticosteroids * 0.37679334437547285
    a += b_cvd * 0.1967261568066525
    a += b_gestdiab * 1.0689325033692647
    a += b_learning * 0.4542293408951035
    a += b_manicschiz * 0.16161718890842605
    a += b_pos * 0.3565365789576717
    a += b_statin * 0.5809287382718668
    a += b_treatedhyp * 0.2836632020122907
    a += fh_diab * 0.4522149766206112

    a += age_1 * b_atypicalantipsy * -0.7683591642786523
    a += age_1 * b_learning * -0.7983128124297588
    a += age_1 * b_statin * -1.9033508839833257
    a += age_1 * bmi_1 * 0.4844747602404915
    a += age_1 * bmi_2 * -0.03193998830718134
    a += age_1 * fbs_1 * 2.244290304740435
    a += age_1 * fbs_2 * 13.006838869978303
    a += age_1 * fh_diab * -0.3040627374034501
    a += age_2 * b_atypicalantipsy * 0.0005194455624413476
    a += age_2 * b_learning * 0.00030283275671618906
    a += age_2 * b_statin * 0.002439711140601871
    a += age_2 * bmi_1 * -0.004157297668215406
    a += age_2 * bmi_2 * 0.0001126882194204252
    a += age_2 * fbs_1 * 0.019934530853431255
    a += age_2 * fbs_2 * -0.07166771875293067
    a += age_2 * fh_diab * 0.0004523639671202325

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score

# Model C
def type2_female_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_gestdiab, b_learning, b_manicschiz, b_pos, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.988788545131683]

    Iethrisk = [
        0,
        0,
        0.5990951599291541,
        0.7832030965635389,
        1.1947351247960103,
        0.7141744699168143,
        0.11953284683887688,
        0.013668872878490427,
        0.5709226537693945,
        0.1709107628106929
    ]
    Ismoke = [
        0,
        0.06584825851000067,
        0.1458413689734224,
        0.15258642474801187,
        0.30787416796613976
    ]

    dage = age / 10
    age_1 = dage ** 0.5
    age_2 = dage ** 3
    dbmi = bmi / 10
    bmi_2 = dbmi ** 3
    bmi_1 = dbmi
    dhba1c = hba1c / 10
    hba1c_1 = dhba1c ** 0.5
    hba1c_2 = dhba1c

    age_1 -= 2.123332023620606
    age_2 -= 91.64474487304688
    bmi_1 -= 2.571253299713135
    bmi_2 -= 16.999439239501953
    hba1c_1 -= 1.886751174926758
    hba1c_2 -= 3.559829950332642
    town -= 0.391116052865982

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 3.565521489194772
    a += age_2 * -0.005615824357273314
    a += bmi_1 * 2.5043028874544841
    a += bmi_2 * -0.04287580189269046
    a += hba1c_1 * 8.736803130736218
    a += hba1c_2 * -0.07823138666994997
    a += town * 0.03586682205634829

    a += b_atypicalantipsy * 0.54976333110422
    a += b_corticosteroids * 0.16872205506389704
    a += b_cvd * 0.16443300362739344
    a += b_gestdiab * 1.125009810517114
    a += b_learning * 0.28912058310739658
    a += b_manicschiz * 0.31825122490684077
    a += b_pos * 0.33806444140981745
    a += b_statin * 0.45593968473811164
    a += b_treatedhyp * 0.4040022295023758
    a += fh_diab * 0.44280154048260317

    a += age_1 * b_atypicalantipsy * -0.8125434197162131
    a += age_1 * b_learning * -0.9084665765269808
    a += age_1 * b_statin * -1.8557960585560658
    a += age_1 * bmi_1 * 0.6023218765235252
    a += age_1 * bmi_2 * -0.03449503839680447
    a += age_1 * fh_diab * -0.2727571351506187
    a += age_1 * hba1c_1 * 25.441203322736715
    a += age_1 * hba1c_2 * -6.807608042155611
    a += age_2 * b_atypicalantipsy * 0.0004665611306005428
    a += age_2 * b_learning * 0.0008518980139928006
    a += age_2 * b_statin * 0.0022627250963352537
    a += age_2 * bmi_1 * -0.004338664566313342
    a += age_2 * bmi_2 * 0.00011627785616712089
    a += age_2 * fh_diab * 0.0004354519795220775
    a += age_2 * hba1c_1 * -0.05225413558859252
    a += age_2 * hba1c_2 * 0.014054825906114453

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score