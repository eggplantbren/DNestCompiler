#ifndef _MyModel_
#define _MyModel_

#include "Model.h"
#include <vector>

class MyModel:public DNest3::Model
{

    private:
        double theta;
        double theta2;
        double x;

    public:

        MyModel();
        void fromPrior();
        double perturb();

        // double logLikelihood() const;
        // void print(std::ostream& out) const;
        // std::string description() const;

};

#endif