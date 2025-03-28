import math

# Model A
def type2_male_raw_a(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.978732228279114]

    Iethrisk = [
        0,
        0,
        1.1000230829124793,
        1.290384012614721,
        1.6740908848727458,
        1.1400446789147816,
        0.46824681690655806,
        0.69905649963015448,
        0.68943657127111568,
        0.41722228467738209
    ]
    Ismoke = [
        0,
        0.16387409105485573,
        0.31851449113958979,
        0.32207266567783432,
        0.45052437163409531
    ]

    dage = age / 10
    age_2 = dage ** 3
    age_1 = math.log(dage)
    dbmi = bmi / 10
    bmi_2 = dbmi ** 3
    bmi_1 = dbmi ** 2

    age_1 -= 1.496392488479614
    age_2 -= 89.048171997070313
    bmi_1 -= 6.817805767059326
    bmi_2 -= 17.801923751831055
    town -= 0.515986680984497

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 4.4642324388691348
    a += age_2 * -0.0040750108019255568
    a += bmi_1 * 0.95129027867120675
    a += bmi_2 * -0.14352488277885475
    a += town * 0.025918182067678725

    a += b_atypicalantipsy * 0.42101092346005436
    a += b_corticosteroids * 0.22183580932925384
    a += b_cvd * 0.20269605756290021
    a += b_learning * 0.23315321407986961
    a += b_manicschiz * 0.22770449520517727
    a += b_statin * 0.58490075431141342
    a += b_treatedhyp * 0.33379392183501078
    a += fh_diab * 0.64799284899369536

    a += age_1 * b_atypicalantipsy * -0.94637722268534152
    a += age_1 * b_learning * -0.93842375526499833
    a += age_1 * b_statin * -1.7479070653003299
    a += age_1 * bmi_1 * 0.45147599241879766
    a += age_1 * bmi_2 * -0.10795481262776381
    a += age_1 * fh_diab * -0.60118530429301198
    a += age_2 * b_atypicalantipsy * -0.0000519927442172335
    a += age_2 * b_learning * 0.00071026438559688141
    a += age_2 * b_statin * 0.0013508364599531669
    a += age_2 * bmi_1 * -0.0011797722394560309
    a += age_2 * bmi_2 * 0.00021471509139319291
    a += age_2 * fh_diab * 0.00049141855940878034

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score

# Model B
def type2_male_raw_b(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fbs, fh_diab, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.985019445419312]

    Iethrisk = [
        0,
        0,
        1.0081475800686235,
        1.3359138425778705,
        1.4815419524892652,
        1.0384996851820663,
        0.52023480708875247,
        0.85796734182585588,
        0.64131089607656155,
        0.48383402208215048
    ]
    Ismoke = [
        0,
        0.11194757923641625,
        0.31101320954122047,
        0.33288984693260421,
        0.42570690269419931
    ]

    dage = age / 10
    age_1 = math.log(dage)
    age_2 = dage ** 3
    dbmi = bmi / 10
    bmi_1 = dbmi ** 2
    bmi_2 = dbmi ** 3
    dfbs = fbs
    fbs_1 = dfbs ** -0.5
    fbs_2 = fbs_1 * math.log(dfbs)

    age_1 -= 1.496392488479614
    age_2 -= 89.048171997070313
    bmi_1 -= 6.817805767059326
    bmi_2 -= 17.801923751831055
    fbs_1 -= 0.448028832674026
    fbs_2 -= 0.719442605972290
    town -= 0.515986680984497

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 4.1149143302364717
    a += age_2 * -0.0047593576668505362
    a += bmi_1 * 0.81693615876442971
    a += bmi_2 * -0.12502377403433362
    a += fbs_1 * -54.841788128097107
    a += fbs_2 * -53.11207849848136
    a += town * 0.025374175519894356

    a += b_atypicalantipsy * 0.44179340888895774
    a += b_corticosteroids * 0.34135473483394541
    a += b_cvd * 0.21589774543727566
    a += b_learning * 0.40128850275853001
    a += b_manicschiz * 0.21817693913997793
    a += b_statin * 0.51476576001117347
    a += b_treatedhyp * 0.24672092874070373
    a += fh_diab * 0.57494373339875127

    a += age_1 * b_atypicalantipsy * -0.95022243138231266
    a += age_1 * b_learning * -0.83583701630900453
    a += age_1 * b_statin * -1.814178691926946
    a += age_1 * bmi_1 * 0.37484820920783846
    a += age_1 * bmi_2 * -0.090983657956248742
    a += age_1 * fbs_1 * 21.011730121764334
    a += age_1 * fbs_2 * 23.824460044746974
    a += age_1 * fh_diab * -0.67806477052916658
    a += age_2 * b_atypicalantipsy * 0.00014729720771628743
    a += age_2 * b_learning * 0.00060129192649664091
    a += age_2 * b_statin * 0.0016393484911405418
    a += age_2 * bmi_1 * -0.0010774782221531713
    a += age_2 * bmi_2 * 0.00019110487304583101
    a += age_2 * fbs_1 * -0.039004607922383527
    a += age_2 * fbs_2 * -0.041127719805895947
    a += age_2 * fh_diab * 0.00062575882488594993

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score

# Model C
def type2_male_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, surv, town):
    surv = 10
    survivor = [0] * 10 + [0.981181740760803]

    Iethrisk = [
        0,
        0,
        0.67571207054987803,
        0.83147325049663456,
        1.0969133802228563,
        0.76822446364560482,
        0.20897529259108502,
        0.38091593781970579,
        0.34235836796612695,
        0.22046477853433083
    ]
    Ismoke = [
        0,
        0.11592891206878651,
        0.14624182637633271,
        0.10781424112493142,
        0.19848629163668474
    ]

    dage = age / 10
    age_1 = math.log(dage)
    age_2 = dage ** 3
    dbmi = bmi / 10
    bmi_1 = dbmi ** 2
    bmi_2 = dbmi ** 3
    dhba1c = hba1c / 10
    hba1c_1 = dhba1c ** 0.5
    hba1c_2 = dhba1c

    age_1 -= 1.496392488479614
    age_2 -= 89.048171997070313
    bmi_1 -= 6.817805767059326
    bmi_2 -= 17.801923751831055
    hba1c_1 -= 1.900265336036682
    hba1c_2 -= 3.611008167266846
    town -= 0.515986680984497

    a = 0

    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * 4.0193435623978031
    a += age_2 * -0.0048396442306278238
    a += bmi_1 * 0.81829168905349325
    a += bmi_2 * -0.12558808701359642
    a += hba1c_1 * 8.0511642238857934
    a += hba1c_2 * -0.14652346893914495
    a += town * 0.025229965184900727

    a += b_atypicalantipsy * 0.45541525220173301
    a += b_corticosteroids * 0.13816187686823922
    a += b_cvd * 0.14546988896239518
    a += b_learning * 0.2596046658040857
    a += b_manicschiz * 0.28523788490585894
    a += b_statin * 0.42551951901185525
    a += b_treatedhyp * 0.33169430006459311
    a += fh_diab * 0.56612325943680619

    a += age_1 * b_atypicalantipsy * -1.0013331909079835
    a += age_1 * b_learning * -0.89164657372215927
    a += age_1 * b_statin * -1.7074561167819817
    a += age_1 * bmi_1 * 0.45074527472672443
    a += age_1 * bmi_2 * -0.10851859809165601
    a += age_1 * fh_diab * -0.61410093887097161
    a += age_1 * hba1c_1 * 27.670593827146565
    a += age_1 * hba1c_2 * -7.4006134846785434
    a += age_2 * b_atypicalantipsy * 0.00022455973985742407
    a += age_2 * b_learning * 0.00066044360765696482
    a += age_2 * b_statin * 0.0013873509357389619
    a += age_2 * bmi_1 * -0.0012224736160287865
    a += age_2 * bmi_2 * 0.0002266731010346126
    a += age_2 * fh_diab * 0.00050602582894772091
    a += age_2 * hba1c_1 * -0.05920145812475433
    a += age_2 * hba1c_2 * 0.015592089485149988

    score = 100.0 * (1 - survivor[surv] ** math.exp(a))
    return score