#ifndef _MyModel_
#define _MyModel_

#include "Model.h"
#include <vector>

class MyModel:public DNest3::Model
{
    private:
        // Data
        static double x;
        
        // Parameters (coordinates on the hypothesis space)
        double mu;
        double sigma;
        double muSq;

        // Derived quantities

    public:

        MyModel();
        void fromPrior();
        double perturb();

        // Proposals for each of the parameters
        double perturb_mu();
        double perturb_sigma();
        double perturb_muSq();

        double logLikelihood() const;
        void print(std::ostream& out) const;
        std::string description() const;

};

#endif