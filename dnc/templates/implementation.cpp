#include "{{ name }}.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include <cmath>

using namespace std;
using namespace DNest3;

{{ name }}::{{ name }}()
{
}

void {{ name }}::fromPrior()
{
    {%- for node in nodes %}
    {%- if node.prior %}
    // Prior on {{ node.name }}
    {{ node.prior.strip() }}
    {% endif %}
    {%- endfor %}
}

double {{ name }}::perturb() {
    double logH = 0.0;

    
    return logH;
}

{% for node in nodes %}
double {{ name }}::perturb_{{ node.name }}()
{
    double logH = 0.;
    {{ node.proposal.strip() }}
    return logH;
}
{% endfor %}

void {{ name }}::print(std::ostream& out) const
{
    {%- for node in nodes %}
    out<<{{ node.name }}<<' ';
    {%- endfor %}
}

string {{ name }}::description() const
{
    string result = "";
    {%- for node in nodes %}
    result += "{{ node.name }}";
    result += ", ";
    {%- endfor %}
    return result;
}

double {{ name }}::logLikelihood() const
{
    double logL = 0.;

    return 0.;
}

