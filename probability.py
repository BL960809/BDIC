from scipy.special import comb, perm

label1 = 4 * comb(13, 5) / comb(52, 5)          # 同花色
label2 = 4 * comb(13, 4) * 3 * comb(13, 1) / comb(52, 5)        # 4 + 1
label3 = 4 * comb(13, 3) * 3 * comb(13, 2) / comb(52, 5)        # 3 + 2
label4 = 4 * comb(13, 3) * 3 * comb(13, 1) * 2 * comb(13, 1) / comb(52, 5) / perm(2, 2)     # 3 + 1 + 1
label5 = 4 * comb(13, 2) * 3 * comb(13, 2) * 2 * comb(13, 1) / comb(52, 5) / perm(2, 2)     # 2 + 2 + 1
label6 = 4 * comb(13, 2) * comb(13, 1) * comb(13, 1) * comb(13, 1) / comb(52, 5)        # 2 + 1 + 1 + 1

a = [label1, label2, label3, label4, label5, label6]
sum(a)

