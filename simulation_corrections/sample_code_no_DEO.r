#!/usr/bin/env Rscript
myargs = commandArgs(trailingOnly=TRUE)



sd_energy = as.numeric(myargs[1])
window = as.numeric(myargs[2])
correction = as.numeric(myargs[3])
our_seed = as.numeric(myargs[4])
lr = as.numeric(myargs[5])

set.seed(our_seed)

mean1 = -4
mean2 = 3
f = function(x) return(-log(0.4 * dnorm(x, mean=mean1, sd=0.7) + 0.6 * dnorm(x, mean=mean2, sd=0.5)))
nosiy_f = function(x) return(f(x) + rnorm(1, 0, sd_energy))


# Important hyperparameters
#lr = 0.01
T_high = 10
T_low = 1

# Other hyperparameters
x_low = 0
x_high = 0
part1 = 100
thinning = 10

# You can set a larger value to obtain more stable results.
total = 10000000


################################################### reSGLD ###################################################
samples_ptsgld = c()
x_low = 0
x_high = 0
counter = 0
window = window
gate = 1 
swaps = 0
for (i in 1:part1) {
    samples_part = c()
    for (j in 1:(total/part1)) {
        if (counter %% window == 0) {
            gate = 1
        }

        x_low  = x_low  - lr * numDeriv::grad(f, x_low)  + sqrt(2 * lr * T_low)  * rnorm(1, 0, 1)
        x_high = x_high - lr * numDeriv::grad(f, x_high) + sqrt(2 * lr * T_high) * rnorm(1, 0, 1)
        
        integrand_corrected = min(1, exp((1 / T_high - 1 / T_low) * (nosiy_f(x_high) - nosiy_f(x_low) - (1 / T_high - 1 / T_low) * sd_energy**2) - correction))
        
        if ((runif(1) < integrand_corrected) & (gate == 1)) {
            tmp = x_low
            x_low = x_high
            x_high = tmp
            gate = 0
            swaps = swaps + 1
        }
        counter = counter + 1
        if (j %% thinning == 0) {samples_part = c(samples_part, x_low)}
    }
    print(i)
    samples_ptsgld = c(samples_ptsgld, samples_part)
}

# burn-In
samples_ptsgld2 = samples_ptsgld[1000: length(samples_ptsgld)]



part_left = as.integer(length(samples_ptsgld2) *0.4)
part_right = length(samples_ptsgld2) - part_left

real_samples = c(rnorm(part_left, mean=mean1, sd=0.7), rnorm(part_right, mean=mean2, sd=0.5))

wdata = data.frame(
        Type = factor(rep(c("Ground truth", "reSGLD"), each=length(samples_ptsgld2))),
        weight = c(real_samples, samples_ptsgld2)
        )

print(c("Number of swaps", swaps))



moving_avg = function(pdf_hist, partition) {
    # create weight funcs
    decay = 0.9
    ww = c(1)
    width = 10
    for (idx in 1:width) {
        ww = c(ww, ww[idx] * decay)
    }
    ww = c(rev(ww[2:length(ww)]), ww)
    # take smoothing average
    new_pdf = c()
    for (idx in (width+1): (partition-(width+1))) {
        smooth_avg = sum(pdf_hist[(idx-width): (idx+width)] * ww) / sum(ww)
        new_pdf = c(new_pdf, smooth_avg)
    }
    new_pdf = c(pdf_hist[1:width], new_pdf, pdf_hist[(length(pdf_hist)-width):length(pdf_hist)])
    return(new_pdf)
}


histogram_pdf = function(samples) {
    left = -7
    right = 6
    partition = 300
    delta = (right - left) / partition
    pdf_hist = c()
    for (idx in 1:partition) {
        boundary_left = left + idx * delta
        boundary_right = left + (idx + 1) * delta
        count = sum((samples >= boundary_left) & (samples < boundary_right))
        pdf_hist = c(pdf_hist, count)
    }
    pdf_hist = pdf_hist / sum(pdf_hist)
    pdf_smooth = moving_avg(pdf_hist, partition)
    #plot(pdf_hist)
    #lines(pdf_smooth)
    return(pdf_smooth)
}


real_hist = histogram_pdf(real_samples)
empi_hist = histogram_pdf(samples_ptsgld2)


# error below 0.036 is a good estimate
print(c("Sum of error", sum(abs(real_hist - empi_hist))))




