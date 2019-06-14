"""
An example demonstrating how to put together a crossfilter app based
on the Auto MPG dataset. Demonstrates how to dynamically generate
bokeh plots using the HoloViews API and replacing the bokeh plot
based on the current widget selections.

Q: How do I export a figure?
A: The easiest way to save a figure is the hv.save utility, which allows saving plots in different 
formats depending on what is supported by the selected backend:
# Using bokeh
hv.save(obj, 'plot.html', backend='bokeh')
#
#

"""

import pandas as pd
import numpy as np
from django.conf import settings
from .models import *


class holoviews_class():
    def __init__(self):
        pass    
        # FOO_ Nothing defined here as of now - lets see what DEFAULTS can be given here..
        from bokeh.models import Range1d
        from bokeh.embed import components
        from bokeh.layouts import row
        from bokeh.plotting import figure, show, output_file
        from bokeh.resources import CDN

    def holoviews_bar_small(self):
        """
        holoviews_bar_small :- 
        Plot the Categorical Cols.
        Plot Cat Cols with Max and Min Categories.
        """
        try:
            import pandas as pd
            import holoviews as hv
            from holoviews import opts
            from bokeh.plotting import figure, show, output_file
            from bokeh.embed import components
            from bokeh.resources import CDN
            from holoviews.core.options import Store
        
            df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
            col_names_fromPSQL =  list(df_for_bokeh)
            ls_SeriesName = []
            ls_SeriesUnqCnts = [] 
            for k in range(len(col_names_fromPSQL)):
                series_name = str(col_names_fromPSQL[k])
                ls_SeriesName.append(series_name)
                unq_values_list = df_for_bokeh[series_name].unique()
                ls_SeriesUnqCnts.append(len(unq_values_list))
            df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts})
            # ls_SeriesUnqCnts -- is COUNT of SUB_CATEGORIES within the CATEGORY = ls_SeriesName
            min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()
            # min_valIndex -- is INDEX of SERIES with LEAST NUMBER of UNIQUE VALUES 
            max_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmax()
            # max_valIndex -- is INDEX of SERIES with MAX NUMBER of UNIQUE VALUES 
            colA_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']
            unq_values_listA = df_for_bokeh[colA_with_CategoricalValues].unique()
            #print("----------unq_values_listA-------------",unq_values_listA)
            
            #key_dimensions   = [('businesstravel', 'BUSINESS_TRAVEL'), ('dailyrate', 'DAILY_RATE')]
            key_dimensions   = [('businesstravel', 'BUSINESS_TRAVEL')]
            value_dimensions = [('dailyrate', 'DAILY_RATE')]
            macro = hv.Table(df_for_bokeh, key_dimensions, value_dimensions)
            bars = macro.to.bars(['businesstravel', 'dailyrate'], 'department', [])
            print("---------type(bars)----1----",type(bars)) ## <class 'holoviews.element.chart.Bars'>

            ##### Below line Commented for TESTING 
            bars.opts(
                opts.Bars(color=hv.Cycle('Category20'), show_legend=False, stacked=True,
                            tools=['hover'], width=600, xrotation=90))
            #### ERROR == AttributeError: type object 'opts' has no attribute 'Bars'

            
            # /dc_dash/dc_holoviews.py", line 65, in holoviews_bar_small
            # bokeh_renderer = Store.renderers['bokeh']
            # KeyError: 'bokeh'

            
            # bokeh_renderer = Store.renderers['bokeh']
            # bokeh_plot = bokeh_renderer.get_plot(bars).state
            # hv.renderer('bokeh').get_plot(bars).state

            print("---------type(bars)----2----",type(bars)) ## <class 'holoviews.element.chart.Bars'>
            #print("---------type(bokeh_plot)-------",type(bokeh_plot))
            #bars.toolbar.logo = None
            #bars.toolbar_location = None
            # FOO_Issue = https://github.com/pyviz/holoviews/issues/1975

            js_holo_bar, div_holo_bar = components(bokeh_plot)
            cdn_js_holo_bar=CDN.js_files[0] # NOT REQD ?? 
            cdn_css_holo_bar=CDN.css_files[0] # NOT REQD ?? 
            return js_holo_bar,div_holo_bar,cdn_js_holo_bar,cdn_css_holo_bar

        except Exception as e:
            print("--Exception as e:---File=>>-dc_holoviews.py-=--def holoviews_bar_small(self)------",e)
            #return  >>>FOO>>>  ## Custom HTML to come here ...
            


    def holoviews_bar_small_old_FOO(self):
        """
        holoviews_bar_small
        """
        import pandas as pd
        import holoviews as hv
        from holoviews import opts
        #### Bokeh Imports
        from bokeh.plotting import figure, show, output_file
        from bokeh.embed import components
        from bokeh.resources import CDN
        from holoviews.core.options import Store
        

        import numpy as np
        import pandas as pd

        index = pd.date_range('1/1/2000', periods=1000)
        df = pd.DataFrame(np.random.randn(1000, 4), index=index, columns=list('ABCD')).cumsum()
        print(df.head(5))
        import hvplot.pandas

        whatis = df.hvplot()
        print("-------whatis----------",whatis)

        """
        :NdOverlay   [Variable]
        :Curve   [index]   (value)
        """

        """
        #try:
        
        
        df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
        #key_dimensions   = [('businesstravel', 'BUSINESS_TRAVEL'), ('dailyrate', 'DAILY_RATE')]
        key_dimensions   = [('businesstravel', 'BUSINESS_TRAVEL')]
        value_dimensions = [('dailyrate', 'DAILY_RATE')]
        macro = hv.Table(df_for_bokeh, key_dimensions, value_dimensions)
        bars = macro.to.bars(['businesstravel', 'dailyrate'], 'department', [])
        print("---------type(bars)----1----",type(bars)) ## <class 'holoviews.element.chart.Bars'>

        ##### Below line Commented for TESTING 
        bars.opts(
            opts.Bars(color=hv.Cycle('Category20'), show_legend=False, stacked=True,
                        tools=['hover'], width=600, xrotation=90))
        #### ERROR == AttributeError: type object 'opts' has no attribute 'Bars'

        
        # /dc_dash/dc_holoviews.py", line 65, in holoviews_bar_small
        # bokeh_renderer = Store.renderers['bokeh']
        # KeyError: 'bokeh'

        
        # bokeh_renderer = Store.renderers['bokeh']
        # bokeh_plot = bokeh_renderer.get_plot(bars).state
        # hv.renderer('bokeh').get_plot(bars).state

        print("---------type(bars)----2----",type(bars)) ## <class 'holoviews.element.chart.Bars'>
        #print("---------type(bokeh_plot)-------",type(bokeh_plot))
        #bars.toolbar.logo = None
        #bars.toolbar_location = None

        """

        js_holo_bar, div_holo_bar = components(bokeh_plot)
        cdn_js_holo_bar=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_holo_bar=CDN.css_files[0] # NOT REQD ?? 
        return js_holo_bar,div_holo_bar,cdn_js_holo_bar,cdn_css_holo_bar

        # except Exception as e:
        #     print("--except Exception as e:---FROM ===>>-dc_holoviews.py--==--def holoviews_bar_small(self)------",e)
        #     #return  >>>  ## Custom HTML to come here ...
            

    def holoviews_violinPlot_small(self):
        """
        holoviews_violinPlot_small
        """
        try:
            #
            import holoviews as hv
            from holoviews import dim
            from bokeh.sampledata.autompg import autompg
            from bokeh.layouts import row, widgetbox
            from bokeh.models import Select , HoverTool
            #from bokeh.models import HoverTool , WheelZoomTool , LassoSelectTool ,BoxZoomTool, ResetTool , PanTool
            from bokeh.plotting import curdoc
            
            #### Bokeh Imports
            from bokeh.plotting import figure, show, output_file
            from bokeh.embed import components
            from bokeh.resources import CDN
            #
            df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")

            hv.extension('bokeh')

            ### OWN EXPERI STARTS ===  businesstravel  dailyrate 
            # label = "WATSON ANALYTICS EMPLOYEE ATTRITION"
            #TBD-- ##label=label

            # violin_plot ==1 ---- BUSINESS_TRAVEL..'DAILY_RATE
            violin_plot = hv.Violin(df_for_bokeh, ('businesstravel', 'BUSINESS_TRAVEL'), ('dailyrate', 'DAILY_RATE')).redim.range(dailyrate=(120, 1300))
            violin_plot.opts(height=200, width=210,show_legend=False, tools=['hover'],violin_fill_color=dim('BUSINESS_TRAVEL').str(), cmap='Set1')
            violin_plot = hv.render(violin_plot)
            #plot_width=150, plot_height=170
            print("---------type(violin_plot)--------",type(violin_plot))
            ##<class 'bokeh.plotting.figure.Figure'>
            violin_plot.toolbar.logo = None
            violin_plot.toolbar_location = None
        
            js_violin_plot, div_violin_plot = components(violin_plot)
            cdn_js_violin_plot=CDN.js_files[0] # NOT REQD ?? 
            cdn_css_violin_plot=CDN.css_files[0] # NOT REQD ?? 

            # violin_plot ==2 ---- BUSINESS_TRAVEL..ATTRITTION -- attrition
            violin_plot1 = hv.Violin(df_for_bokeh, ('businesstravel', 'BUSINESS_TRAVEL'), ('attrition', 'ATTRITION')).redim.range(attrition=(0,1))
            violin_plot1.opts(height=200, width=210,show_legend=False,tools=['hover'], violin_fill_color=dim('BUSINESS_TRAVEL').str(), cmap='Set1')
            violin_plot1 = hv.render(violin_plot1)
            print("---------type(violin_plot)--------",type(violin_plot1))
            ##<class 'bokeh.plotting.figure.Figure'>
            violin_plot1.toolbar.logo = None
            violin_plot1.toolbar_location = None
        
            js_violin_plot1, div_violin_plot1 = components(violin_plot1)
            cdn_js_violin_plot1=CDN.js_files[0] # NOT REQD ?? 
            cdn_css_violin_plot1=CDN.css_files[0] # NOT REQD ?? 
            return js_violin_plot,div_violin_plot,cdn_js_violin_plot,cdn_css_violin_plot , js_violin_plot1,div_violin_plot1,cdn_js_violin_plot1,cdn_css_violin_plot1

        except Exception as e:
            print("--except Exception as e:---FROM ===>>-dc_holoviews.py--==--def holoviews_violinPlot_small(self)------",e)
            #return  >>>  ## Custom HTML to come here ...
            """
            FOO_ERROR --- 10 JUNE ---
            --except Exception as e:---FROM ===>>-dc_holoviews.py--==--def holoviews_violinPlot_small(self)------ Supplied data does not contain specified dimensions, the following dimensions were not found: ['businesstravel', 'dailyrate']
            PandasInterface expects tabular data, for more information on supported datatypes see http://holoviews.org/user_guide/Tabular_Datasets.html

            """

        
    def holoviews_violinPlot_large(self):
        import holoviews as hv
        from holoviews import dim
        from bokeh.sampledata.autompg import autompg
        from bokeh.layouts import row, widgetbox
        from bokeh.models import Select
        from bokeh.plotting import curdoc
        
        #### Bokeh Imports
        from bokeh.plotting import figure, show, output_file
        from bokeh.embed import components
        from bokeh.resources import CDN

        df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
        hv.extension('bokeh')
        ### OWN EXPERI STARTS ===  businesstravel  dailyrate 
        # label = "WATSON ANALYTICS EMPLOYEE ATTRITION"
        #TBD-- ##label=label

        # violin_plot ==1 ---- BUSINESS_TRAVEL..'DAILY_RATE
        violin_plot = hv.Violin(df_for_bokeh, ('businesstravel', 'BUSINESS_TRAVEL'), ('dailyrate', 'DAILY_RATE')).redim.range(dailyrate=(120, 1300))
        violin_plot.opts(height=500, width=900,show_legend=True, violin_fill_color=dim('BUSINESS_TRAVEL').str(), cmap='Set1')
        violin_plot = hv.render(violin_plot)
        print("---------type(violin_plot)--------",type(violin_plot))
        ##<class 'bokeh.plotting.figure.Figure'>
        js_violin_plot, div_violin_plot = components(violin_plot)
        cdn_js_violin_plot=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_violin_plot=CDN.css_files[0] # NOT REQD ?? 

        # violin_plot ==2 ---- BUSINESS_TRAVEL..ATTRITTION -- attrition
        violin_plot1 = hv.Violin(df_for_bokeh, ('businesstravel', 'BUSINESS_TRAVEL'), ('attrition', 'ATTRITION')).redim.range(attrition=(0,1))
        violin_plot1.opts(height=500, width=900,show_legend=True, violin_fill_color=dim('BUSINESS_TRAVEL').str(), cmap='Set1')
        violin_plot1 = hv.render(violin_plot1)
        print("---------type(violin_plot)--------",type(violin_plot1))
        ##<class 'bokeh.plotting.figure.Figure'>
        js_violin_plot1, div_violin_plot1 = components(violin_plot1)
        cdn_js_violin_plot1=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_violin_plot1=CDN.css_files[0] # NOT REQD ?? 

        return js_violin_plot,div_violin_plot,cdn_js_violin_plot,cdn_css_violin_plot , js_violin_plot1,div_violin_plot1,cdn_js_violin_plot1,cdn_css_violin_plot1

        














        



    # def holoviews_plot_1(self):
    #     #
    #     """
    #     #Working Code - OK -- ORIGINAL -- Cars MPG Example -Not Reqd-- dc_holoviews_plotview
    #     """
    #     import holoviews as hv
    #     from bokeh.layouts import row, widgetbox
    #     from bokeh.models import Select
    #     from bokeh.plotting import curdoc
    #     from bokeh.sampledata.autompg import autompg
    #     #### Bokeh Imports
    #     from bokeh.plotting import figure, show, output_file
    #     from bokeh.embed import components
    #     from bokeh.resources import CDN

        
    #     df = autompg.copy()

    #     SIZES = list(range(6, 22, 3))
    #     ORIGINS = ['North America', 'Europe', 'Asia']

    #     # data cleanup
    #     df.cyl = [str(x) for x in df.cyl]
    #     df.origin = [ORIGINS[x-1] for x in df.origin]

    #     df['year'] = [str(x) for x in df.yr]
    #     del df['yr']

    #     df['mfr'] = [x.split()[0] for x in df.name]
    #     df.loc[df.mfr=='chevy', 'mfr'] = 'chevrolet'
    #     df.loc[df.mfr=='chevroelt', 'mfr'] = 'chevrolet'
    #     df.loc[df.mfr=='maxda', 'mfr'] = 'mazda'
    #     df.loc[df.mfr=='mercedes-benz', 'mfr'] = 'mercedes'
    #     df.loc[df.mfr=='toyouta', 'mfr'] = 'toyota'
    #     df.loc[df.mfr=='vokswagen', 'mfr'] = 'volkswagen'
    #     df.loc[df.mfr=='vw', 'mfr'] = 'volkswagen'
    #     del df['name']

    #     columns = sorted(df.columns)
    #     print("---------COLUMNS ==-----",columns)
    #     discrete = [x for x in columns if df[x].dtype == object]
    #     continuous = [x for x in columns if x not in discrete]
    #     quantileable = [x for x in continuous if len(df[x].unique()) > 20]
    #     print("---------quantileable----",quantileable)

    #     renderer = hv.renderer('bokeh')
    #     print("----------HOLOVIEWS -----",renderer)
    #     ##  BokehRenderer()
    #     #
    #     options = hv.Store.options(backend='bokeh')
    #     options.Points = hv.Options('plot', width=800, height=500, size_index=None,) ## OK works 
    #     options.Points = hv.Options('style', cmap='rainbow', line_color='black')

    #     def create_figure():
    #         x = Select(title='X-Axis', value='mpg', options=quantileable)
    #         ## Select == /home/dhankar/anaconda2/lib/python2.7/site-packages/bokeh/models/widgets/inputs.py

    #         #x.on_change('value', update)

    #         y = Select(title='Y-Axis', value='hp', options=quantileable)
    #         #y.on_change('value', update)

    #         #size = Select(title='Size', value='None', options=['None'] + quantileable)
    #         size = Select(title='Size', value='None', options=['None'] + quantileable)
    #         #size.on_change('value', update)

    #         color = Select(title='Color', value='None', options=['None'] + quantileable)
    #         #color.on_change('value', update)


    #         label = "Plot MAIN TITLE == %s vs %s" % (x.value.title(), y.value.title())
    #         kdims = [x.value, y.value]
    #         print("---------TYPE === kdims----------",type(kdims)) ##<class 'list'>
    #         print("--------- kdims----------",kdims) ## ['mpg', 'hp']

    #         opts, style = {}, {}
    #         opts['color_index'] = color.value if color.value != 'None' else None
    #         if size.value != 'None': ## DHANKAR --- CHANGED --- != TO == 
    #             opts['size_index'] = size.value
    #             opts['scaling_factor'] = (1./df[size.value].max())*200
    #             print("-----------AAAA--opts--",opts) ## This line Doesnt print --- this Code doesnt get into this -- - if -- Statement 
    #         print("-----------TYPE--opts--",type(opts)) ## <class 'dict'>
    #         print("-----------BBBB--opts--",opts) ## {'color_index': None} ## Dict value printed outside the -- if -- Statement 
    #         #points = hv.Points(df, kdims=kdims, label=label).opts(plot=opts, style=style) ## Original Code
    #         #points = hv.Points(df, vdims=['mfr', 'size'] , tools=['hover'] , kdims=kdims, label=label).opts(color='mfr') 
    #         """
    #         Supplied data does not contain specified dimensions, the following dimensions were not found: ['size']
    #         PandasInterface expects tabular data, for more information on supported datatypes see http://holoviews.org/user_guide/Tabular_Datasets.html
    #         """
    #         #points = hv.Points(df, vdims=['mfr'] , tools=['hover'] , kdims=kdims, label=label).opts(color='mfr') 
    #         ## WARNING:param.Points01326: Setting non-parameter attribute tools=['hover'] using a mechanism intended only for parameters

    #         points = hv.Points(df, vdims=['mfr'] , kdims=kdims, label=label).opts(color='mfr') 


    #         """
    #         File "pandas/_libs/hashtable_class_helper.pxi", line 1500, in pandas._libs.hashtable.PyObjectHashTable.get_item
    #         KeyError: 'None'

    #         """

    #         # FOO--- Dhankar Code 
    #         from bokeh.io import show
    #         from bokeh.models.tickers import FixedTicker

    #         from bokeh.themes import built_in_themes
    #         from bokeh.io import curdoc

    #         curdoc().theme = 'dark_minimal'

    #         bokeh_plot = hv.render(points)
    #         print("---------type(bokeh_plot)--------",type(bokeh_plot))
    #         ##<class 'bokeh.plotting.figure.Figure'>
    #         #bokeh_plot -- SHOW 
    #         #show(bokeh_plot)
    #         #
    #         #hv.save(bokeh_plot, 'bokeh_plot.png')

    #         #return renderer.get_plot(points).state  ## Original Code 
    #         #return renderer.get_plot(points).state , bokeh_plot  ## ERROR - we are intentionally Returning a TUPLE 
    #         return bokeh_plot  #OWN EXPERI ## ERROR - we are intentionally Returing a TUPLE 

    #     bokeh_plot = create_figure()

    #     js_boxplot, div_boxplot = components(bokeh_plot)
    #     cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
    #     cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 

    #     return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot



        """
        ### Original Code BElow ----------- OK 

        def update(attr, old, new):
            layout.children[1] = create_figure()

        x = Select(title='X-Axis', value='mpg', options=quantileable)
        x.on_change('value', update)

        y = Select(title='Y-Axis', value='hp', options=quantileable)
        y.on_change('value', update)

        size = Select(title='Size', value='None', options=['None'] + quantileable)
        size.on_change('value', update)

        color = Select(title='Color', value='None', options=['None'] + quantileable)
        color.on_change('value', update)

        controls = widgetbox([x, y, color, size], width=200)
        layout = row(controls, create_figure()) ## Original Code --- Commented Out as gives ERROR - we are intentionally Returing a TUPLE 
        print("----------layout---------",layout)
        print("------TYPE----layout---------",type(layout))
        
        #----------layout--------- Row(id='1138', ...)
        #------TYPE----layout--------- <class 'bokeh.models.layouts.Row'>

        
        curdoc().add_root(layout)           ## Original Code --- Commented Out as gives ERROR - we are intentionally Returing a TUPLE 
        curdoc().title = "Crossfilter"       ## Original Code --- Commented Out as gives ERROR - we are intentionally Returing a TUPLE 
        print("---curdoc()--------------",curdoc()) ## <bokeh.document.document.Document object at 

        ### FOO_ERROR --- Some issue with -- curdoc() == https://github.com/bokeh/bokeh/issues/8020

        """
        # ---curdoc()-------------- <bokeh.document.document.Document object at 0x7f778e77f6d8>
        # WARNING:bokeh.embed.util:
        # You are generating standalone HTML/JS output, but trying to use real Python
        # callbacks (i.e. with on_change or on_event). This combination cannot work.

        # Only JavaScript callbacks may be used with standalone output. For more
        # information on JavaScript callbacks with Bokeh, see:

        #     http://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html

        # Alternatively, to use real Python callbacks, a Bokeh server application may
        # be used. For more information on building and running Bokeh applications, see:

        #     http://bokeh.pydata.org/en/latest/docs/user_guide/server.html

        """
        bokeh_dcoument_object = curdoc()
        #js_boxplot, div_boxplot = components(bokeh_dcoument_object)
        
        #layout
        js_boxplot, div_boxplot = components(layout)
        print("----------BOKEH -------js_boxplot---",js_boxplot)
        print("    "*90)

        cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 

        return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot

 
        #### Own Experi Below --- NOT OK - Shows only Black n White Bokeh Scatter of MPG 
        #bokeh_plot
        # bokeh_plot = create_figure()
        # js_boxplot, div_boxplot = components(bokeh_plot)
        # print("----------BOKEH -------js_boxplot---",js_boxplot)
        # print("    "*90)

        # cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
        # cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 

        return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot







        # # Using bokeh
        # p = hv.render(obj, backend='bokeh')
        """

