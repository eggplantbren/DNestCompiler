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
double perturb_{{ node.name }}()
{
    {{ node.proposal.strip() }}
}
{% endfor %}

void {{ name }}::print(std::ostream& out) const
{
    {%- for node in nodes %}
    out<<{{ node.name }}<<' ';
    {%- endfor %}
}

