#poisson scattering
# x = number of pixels with x photons
# num.pixel = number of pixels in total

#intrinsic
num.pixel = 1600

# m = number of incident photons
m = c(0:1000)
avg.hit.least1 = num.pixel*(1-exp(-m/num.pixel))
# use num.pixel from average number of pixels with at least 1 photon
area.MPPC = (1.3E-3)^2
area.pixel = (10E-6)^2


# p = probability that any of subsquares with hitting once
#p = dbinom(1,m,1/num.pixel)

# mu = average # of photons hitting MPPC in the specific interval
mu = m*(1/num.pixel)
#mu = avg.hit.least1*(m/num.pixel)*exp(-m/num.pixel)

# infinitesimal time length (could be pulse width against recov time)c
time.recov = 80E-9
subinterval = time.recov
interval = 10E-9
param.poisson = avg.hit.least1/num.pixel

# alternative param.poisson 
#param.poisson = m*exp(-m/num.pixel)*(area.pixel/area.MPPC)*(subinterval/interval)

p.0 = dpois(0, param.poisson)
p.1 = dpois(1, param.poisson)

p.satu = 1- (p.0 + p.1)


#100*p.satu
#m = 1000 -> 0.00429
#m = 5000 -> 0.01804976

prob_satu = data.frame(
  incident = m,
  probability = p.satu,
  percentage = p.satu*100)

prob_satu$det = prob_satu$incident - (prob_satu$incident*prob_satu$probability)

prob_bin = data.frame(incident = m,
                      det = num.pixel*(1-exp(-m/num.pixel)))


det_compare = abs(prob_satu$det - prob_bin$det)

library(ggplot2)
#p_base = ggplot(data = prob_satu, mapping = aes(x = incident, y = percentage)) + 
  #geom_point(size = 0.001) + geom_line( )
#p_label = p_base + labs(title = "the probability distirubtion of the saturation",
                        #caption = "parameter = product of N_seed and probability that any of pixels is hit by 1 photon",
                        #x = "N_seed", y = "probability")
#p_label

p_base = ggplot(data = prob_satu, aes(x = incident, y = det)) + 
  geom_point(size = 0.001)
p_bin = ggplot(data = prob_bin, aes(x = incident, y = det)) + 
  geom_point(size = 0.001)

p_label = p_base + labs(title = "theoritical detected number of photons",
                        caption = "number of photons on each pixel is assumed as identical and mutually independent distribution (iid)",
                        subtitle = "parameter: average # of pixels hit at least 1 photon",
                        x = "N_seed", y = "N_det")
#probability that each pixel contains more than 2 photons corresponding to each N_seed
p_label

p_both = ggplot() + geom_line(data = prob_satu, aes(x = incident, y = det), color = "red") + 
  geom_line(data = prob_bin, aes(x = incident, y = det), color = "blue") +
  xlab("N_seed") + ylab("N_det")

p_compare = p_both + labs(title = "theoritical detected number of photons",
                     subtitle = "parameter: average # of pixels hit at least 1 photon",
                     x = "N_seed", y = "N_det") + theme_bw(base_family = "HiraKakuProN-W3") 

p_compare





#p_base = ggplot(data = prob_satu, mapping = aes(x = incident, y = percentage) + 
  #geom_point(size = 0.001)
#p_label = p_base + labs(title = "the probability distirubtion of the saturation (each pixel)",
                        #caption = "number of photons on each pixel is assumed as identical and mutually independent distribution (iid)",
                        #subtitle = "parameter: average # of pixels hit at least 1 photon (interval = 80/80ns)",
                        #x = "N_seed", y = "probability")
  #need to change m and incident to 500
