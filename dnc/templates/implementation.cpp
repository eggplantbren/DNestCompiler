#include "{{ name }}.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include <cmath>

using namespace std;
using namespace DNest3;

// Data
{%- for d in data %}
{{ d._ctype }} {{ name }}::{{ d.name }} = {{ d.observed }};
{%- endfor %}


{{ name }}::{{ name }}()
{
}

void {{ name }}::fromPrior()
{
    {%- for param in params %}
    {%- if param.prior %}
    // Prior on {{ param.name }}
    {{ param.prior.strip() }}
    {% endif %}
    {%- endfor %}
}

double {{ name }}::perturb()
{
    double logH = 0.;

    // Propose each parameter with this probability
    double prob = randomU();
    int count = 0;

    do
    {
        {%- for param in params %}
        {%- if param.is_derived == False %}
        if(randomU() <= prob)
        {
		if(randomU() <= 0.5)
		    logH += perturb_{{ param.name }}_1();
		else
		    logH += perturb_{{ param.name }}_2();  
            count++;
        }
        {%- endif %}
        {%- endfor %}

    }while(count == 0);

    return logH;
}

{%- for param in params %}
{%- if param.is_derived == False %}
double {{ name }}::perturb_{{ param.name }}_1()
{
    double logH = 0.;
    {{ param.proposal1.strip() }}
    return logH;
}
{%- endif %}
{%- endfor %}


{%- for param in params %}
{%- if param.is_derived == False %}
double {{ name }}::perturb_{{ param.name }}_2()
{
    double logH = 0.;
    double logP1 = 0.;
    double logP2 = 0.;
    {{ param.proposal2.strip() }}
    logH += logP2 - logP1;
    return logH;
}
{%- endif %}
{%- endfor %}


void {{ name }}::print(std::ostream& out) const
{
    {%- for param in params %}
    out<<{{ param.name }}<<' ';
    {%- endfor %}
}

string {{ name }}::description() const
{
    string result = "";
    {%- for param in params %}
    result += "{{ param.name }}";
    result += ", ";
    {%- endfor %}
    return result;
}

double {{ name }}::logLikelihood() const
{
    double logL = 0.;
    {%- for d in data %}
    {{ d.logprob }}
    {%- endfor %}
    return logL;
}

