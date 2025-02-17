# Run this with bokeh 2.2.3 or 3.6.3 to get two different outputs. The output from 2.2.3 is the desired state
# I've created this example to demonstrate the final layout that my program is creating so it may look more
# complicated than it needs to be but I wanted it to be a fair example. The DOM and template are accurate to
# the output of my program.

from bokeh import __version__ as v
import bokeh.plotting as bk
from bokeh.util.browser import view
from bokeh.layouts import column, row
from bokeh.models import widgets as w
from bokeh.models import css as c
from bokeh.models import CustomJS
from bokeh.io import curdoc


if v == '2.2.3':
    from bokeh.models.widgets import Tabs
    from bokeh.models import Panel
else:
    from bokeh.models import Tabs
    from bokeh.models import TabPanel as Panel

template ="""

{% block postamble %}
<style>

    .bk-root .bk .bk.bk-tabs-header.bk-left .bk.bk-headers-wrapper {
    overflow: scroll;
    overflow-x: hidden;
    }

    .bk-root .bk .bk.bk-tabs-header.bk-left .bk.bk-btn-group {
    display: none;
    }

    .bk-root .bk-tabs-header .bk-tab.bk-active{
        font-weight: bold;
        tabindex="0";

    }

</style>
{% endblock %}
"""


x = list(range(11))
y0 = x

l = list()
for i in range(25):
    s1 = bk.figure(frame_width=1000,frame_height=500)
    p = s1.scatter(x, y0)
    panel = Panel(child=column(s1))
    panel.title = f'Plot #{i+1}'
    l.append(panel)

slider = w.Slider(start=0, end=500, value=0, step=1, orientation='horizontal')
slider.width = 400
slider.height = 50

left_tabs = Tabs()
left_tabs.tabs = l
left_tabs.tabs_location = 'left'

left_tabs.visible = False
slider.value = 40

callback = CustomJS(args=dict(left_tabs=left_tabs, slider=slider), code="""
        if (slider.value > 100) {
            left_tabs.tabs.visible = true;  // Show the tab after scrolling
        } else {
            left_tabs.tabs.visible = false;  // Hide the tab if scroll position is less than 100
        }
    );
""")

slider.js_on_change('value', callback)


main_panel = Panel(child=column(left_tabs,slider))
main_panel.title='Plots'

top_tabs = Tabs()
top_tabs.tabs.append(main_panel)

bk.output_file('output.html')

bk.save(top_tabs,template=template)
view('output.html')