setwd('D:/lehui/BDIC/Data')

df = read.csv('Count.csv', header = T)
rownames(df) = df[, 1]
df = df[, -1]

# 组合
comb = function(m, n) {
  
  return(choose(m, n))
}
# 排列
perm = function(m, n) {
  
  return(choose(m, n) * factorial(n))
}

# 计算不同花色组合出现的概率
color_type1 = 4 * comb(13, 5) / comb(52, 5)
color_type2 = 4 * comb(13, 4) * 3 * comb(13, 1) / comb(52, 5)
color_type3 = 4 * comb(13, 3) * 3 * comb(13, 2) / comb(52, 5)
color_type4 = 4 * comb(13, 3) * 3 * comb(13, 1) * 2 * comb(13, 1) / comb(52, 5) / perm(2, 2)
color_type5 = 4 * comb(13, 2) * 3 * comb(13, 2) * 2 * comb(13, 1) / comb(52, 5) / perm(2, 2)
color_type6 = 4 * comb(13, 2) * comb(13, 1) * comb(13, 1) * comb(13, 1) / comb(52, 5)

color_prob = c(color_type1, color_type2, color_type3, color_type4, color_type5, color_type6)


# 卡方检验
chi_test = function(data, prob, alpha) {
  if(TRUE %in% (data < 5)) {
    data = data + 5
  }
  exp = sum(data) * prob
  chi_square = (data - exp)^2 / exp
  chi_square_critical = qchisq(1 - alpha, length(data) - 1)
  
  likelihood = c()
  for(i in 1:length(data)) {
    likelihood = c(likelihood, -2 * data[i] * log(sum(data) * prob[i] / data[i]))
  }
  
  return(list(chi.square = sum(chi_square),
              Likelihood = sum(likelihood),
              chi.square.critical = chi_square_critical,
              p.value = pchisq(sum(chi_square), length(data) - 1, lower.tail = F)))
}

data = df[c(2:6), 1]
chi_test(data, color_prob[2:6], alpha = 0.01)

data = df[c(2:6), 3]
chi_test(data, color_prob[2:6], alpha = 0.01)

data = df[c(3:6), 5]
chi_test(data, color_prob[3:6], alpha = 0.01)

data = df[c(4:6), 7]
chi_test(data, color_prob[4:6], alpha = 0.01)

data = df[c(2:6), 9]
chi_test(data, color_prob[2:6], alpha = 0.01)

data = df[c(4:6), 10]
chi_test(data, color_prob[4:6], alpha = 0.01)





