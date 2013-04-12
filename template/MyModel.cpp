#include "MyModel.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include <cmath>

using namespace std;
using namespace DNest3;

// Data
double MyModel::x = 3.141;


MyModel::MyModel()
{
}

void MyModel::fromPrior()
{
    // Prior on mu
    mu = -10.0 + (10.0 - -10.0)*randomU();
    
    // Prior on sigma
    sigma = exp(log(0.001) + log(1.0/0.001)*randomU());
    
    // Prior on muSq
    muSq = pow(mu, 2);
    
}

double MyModel::perturb()
{
    double logH = 0.;

    // Propose each parameter with this probability
    double prob = randomU();
    int count = 0;

    do
    {
        if(randomU() <= prob)
        {
            logH += perturb_mu();
            count++;
        }
        if(randomU() <= prob)
        {
            logH += perturb_sigma();
            count++;
        }
    }while(count == 0);

    return logH;
}
double MyModel::perturb_mu()
{
    double logH = 0.;
    mu += (10.0 - -10.0)*pow(10., 1.5 - 6.*randomU())*randn();
    mu = mod(mu - -10.0, 10.0 - -10.0) + -10.0;
    muSq = pow(mu, 2);
    return logH;
}
double MyModel::perturb_sigma()
{
    double logH = 0.;
    sigma = log(sigma);
    sigma += log(1.0/0.001)*pow(10., 1.5 - 6.*randomU())*randn();
    sigma = mod(sigma - log(0.001), log(1.0/0.001)) + log(0.001);
    sigma = exp(sigma);
    return logH;
}

void MyModel::print(std::ostream& out) const
{
    out<<mu<<' ';
    out<<sigma<<' ';
    out<<muSq<<' ';
}

string MyModel::description() const
{
    string result = "";
    result += "mu";
    result += ", ";
    result += "sigma";
    result += ", ";
    result += "muSq";
    result += ", ";
    return result;
}

double MyModel::logLikelihood() const
{
    double logL = 0.;
    
    logL += -0.5*log(2*M_PI) - log(sigma) - 0.5*pow((x-mu)/sigma, 2);
    
    return logL;
}
