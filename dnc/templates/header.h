#ifndef _{{ name }}_
#define _{{ name }}_

#include "Model.h"
#include <vector>

class {{name}}:public DNest3::Model
{
    private:
        // Data
        {%- for d in data %}
        static {{ d._ctype }} {{ d.name }};
        {%- endfor %}
        
        // Parameters (coordinates on the hypothesis space)
        {%- for param in params %}
        {{ param._ctype }} {{ param.name }};
        {%- endfor %}

        // Derived quantities
        {%- for d in derived %}
        {{ d._ctype }} {{ d.name }};
        {%- endfor %}

    public:

        {{ name }}();
        void fromPrior();
        double perturb();

        // Proposals for each of the parameters
        {%- for param in params %}
        double perturb_{{ param.name }}_1();
	double perturb_{{ param.name }}_2();
        {%- endfor %}

        double logLikelihood() const;
        void print(std::ostream& out) const;
        std::string description() const;

};

#endif
