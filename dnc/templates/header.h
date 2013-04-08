#ifndef _{{ name }}_
#define _{{ name }}_

#include "Model.h"
#include <vector>

class {{name}}:public DNest3::Model
{

    private:

        {%- for node in nodes %}
        {{ node._ctype }} {{ node.name }};
        {%- endfor %}

    public:

        {{ name }}();
        void fromPrior();
        double perturb();

        // double logLikelihood() const;
        // void print(std::ostream& out) const;
        // std::string description() const;

};

#endif
