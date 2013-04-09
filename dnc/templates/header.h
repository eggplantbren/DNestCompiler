#ifndef _{{ name }}_
#define _{{ name }}_

#include "Model.h"
#include <vector>

class {{name}}:public DNest3::Model
{
    private:
        {%- for param in params %}
        {{ param._ctype }} {{ param.name }};
        {%- endfor %}

        {%- for d in derived %}
        {{ d._ctype }} {{ d.name }};
        {%- endfor %}

        void compute_derived();

    public:

        {{ name }}();
        void fromPrior();
        double perturb();

        {% for param in params %}
        double perturb_{{ param.name }}();
        {%- endfor %}

        double logLikelihood() const;
        void print(std::ostream& out) const;
        std::string description() const;

};

#endif
