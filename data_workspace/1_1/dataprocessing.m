clear

a = csvread('trudata.csv');
a(1,:) = [];
vals = a(:,3);
v = reshape(vals,100,max(a(:,1)));

maxes = max(v);
means = mean(v);

plot(maxes,'linewidth',2)
legend('\fontsize{20} g_{max}')
xlabel('pokolenie',"fontsize", 20)
ylabel('g(x_1, x_2, x_3, x_4)',"fontsize", 20)
figure(2)
plot(means,'-.','linewidth',2)
legend('\fontsize{20} g_{avg}')
xlabel('pokolenie',"fontsize", 20)
ylabel('g(x_1, x_2, x_3, x_4)',"fontsize", 20)

csvwrite('maxmean.csv',[maxes', means'])