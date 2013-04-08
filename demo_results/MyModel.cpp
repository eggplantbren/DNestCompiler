#include "MyModel.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include <cmath>

using namespace std;
using namespace DNest3;

MyModel::MyModel()
{
}

void MyModel::fromPrior()
{
    // Prior on theta
    theta = 0.0 + (1.0 - 0.0) * randomU();
    
    // Prior on theta2
    theta2 = pow(theta, 2);
    
    // Prior on x
    x = theta2 + 0.5 * randn();
    
}

void MyModel::perturb() {
    double logH = 0.0;
    
    // Perturb theta
    theta += (1.0 - 0.0) * pow(10., 1.5-6.*randomU()) * randn();
    theta = mod(theta - 0.0, 1.0 - 0.0);
    
    // Perturb theta2
    theta2 = pow(theta, 2);
    
    // Perturb x
    double _dnc_x = (x - theta2) / 0.5;
    logH += 0.5 * pow(_dnc_x, 2);
    _dnc_x += 0.5 * pow(10., 1.5-6.*randomU()) * randn();
    logH -= 0.5 * pow(_dnc_x, 2);
    x = theta2 + 0.5 * _dnc_x;
    
    return logH;
}