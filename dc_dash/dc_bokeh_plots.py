## FOO_APR_19 Onwards , pip installed version of BOKEH ==> bokeh==0.12.3
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show, ColumnDataSource #,HoverTool ## ImportError: cannot import name 'HoverTool'
from bokeh.models import Range1d
from bokeh.embed import components
from bokeh.resources import CDN
#
import pandas as pd
import numpy as np
from django.conf import settings
from .models import *
from .dc_holoviews import *
#

class bokeh_class():
    def __init__(self):
        pass        
        
    def bokeh_boxplot_large_userInputs(self,col_with_CategoricalValues): #
        #print("--FILE_dc_bokeh_plots=INDEX of dataTables.js Col- clicked as User_input =col_with_CategoricalValues--",col_with_CategoricalValues)
        
        df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
        ## yes_x_range --->>  Identify the CATEGORICAL Column ---- then get UNiQUE FACTORS or CATEGORIES --- pass them as x_range to BOKEH FIGURE
        #  cats = list(df_for_bokeh) #
        ## LIST of COL NAMES from DF --- this is NOT OK --- we need --- yes_x_range --- as defined above. 

        
        #FOO_MAIN_GUESS the CATEGORICAL COLUMN  - Count Unique values in Each Column -- See which Column is categorical / Ordinal / Continous variable etc ...
        # col_names_fromPSQL =  list(df_for_bokeh)
        # #print("----Bokeh large BoxPlot-------col_names_fromPSQL------------",col_names_fromPSQL)
        # ls_SeriesName = []
        # ls_SeriesUnqCnts = [] 
        # for k in range(len(col_names_fromPSQL)):
        #     series_name = str(col_names_fromPSQL[k])
        #     ls_SeriesName.append(series_name)
        #     unq_values_list = df_for_bokeh[series_name].unique()
        #     #print("----BOKEH BoxPlot_LARGE----unq_values_list--------",unq_values_list)
        #     #print(len(unq_values_list))
        #     ls_SeriesUnqCnts.append(len(unq_values_list))
        # df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts})
        # print(df_calcUnq)
        # print("    "*90)
        # min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()
        # ## Above == min_valIndex --- is the INDEX of the SERIES with LEAST NUMBER of UNIQUE VALUES 
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']
        #print(col_with_CategoricalValues)
        #print("    "*90)
        #
        unq_values_list_final = df_for_bokeh[col_with_CategoricalValues].unique()
        
        groups = df_for_bokeh.groupby(str(col_with_CategoricalValues))
        q1 = groups.quantile(q=0.25) # print("-------------q1-----------------",q1) #
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75) 
        iqr = q3 - q1
        upper = q3 + 1.5*iqr #print("------------GROUPS ---- UPPER -------------",upper)
        lower = q1 - 1.5*iqr #print("------------GROUPS ---- LOWER -------------",lower)
        
        col_names_fromPSQL = list(df_for_bokeh) #
        ls_SeriesName = []
        ls_SeriesUnqCnts = [] 
        for k in range(len(col_names_fromPSQL)):
            series_name = str(col_names_fromPSQL[k])
            ls_SeriesName.append(series_name)
            unq_values_list = df_for_bokeh[series_name].unique() #print("---unq_values_list----",unq_values_list)
            ls_SeriesUnqCnts.append(len(unq_values_list))
        df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts}) #print(df_calcUnq)
        min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()  ## this -- min_valIndex --- is INDEX of SERIES with LEAST NUMBER of UNIQUE VALUES 
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']         #print(col_with_CategoricalValues)
        unq_values_list_final = df_for_bokeh[col_with_CategoricalValues].unique()
        list_of_other_Cols = []
        for k in range(len(col_names_fromPSQL)):
            if str(col_names_fromPSQL[k]) == col_with_CategoricalValues:
                pass
            else:
                list_of_other_Cols.append(str(col_names_fromPSQL[k]))
        # Get the UNIQUE Categories from SEGMENTS 
        unq_segments_list = df_for_bokeh[col_with_CategoricalValues].unique() #
        # find the outliers for each category
        def outliers(group):
            unq_segments_list = df_for_bokeh[col_with_CategoricalValues].unique() #
            values_col = list_of_other_Cols[0] #
            
            for k in range(len(unq_segments_list)): ## Getting only 2 categories --- may need a RANGE == LENgth + 1 etc .etc ..
                cat = unq_segments_list[k] #
            return group[(group[values_col] > upper.loc[cat][values_col])][values_col]

        out = groups.apply(outliers).dropna()
        # prepare outlier data for plotting, we need coordinates for every outlier.
        if not out.empty:
            outx = []
            outy = []
            for keys in out.index:
                outx.append(keys[0])
                outy.append(out.loc[keys[0]].loc[keys[1]])
        TOOLTIPS = """
            <div style="background-color:orange;">
                <div>
                    <span style="font-size: 15px; color: #966;">@cats</span>
                </div>
                
                <div>
                    <span style="font-size: 10px; color: black;">($y{int})</span>
                </div>
            </div>
        """                        
        # The --- unq_segments_list --- defined above. 
        cats = unq_segments_list
        ## The --- list_of_other_Cols --- defined above. 
        values_col = list_of_other_Cols[0] #
        ### As per Answer to Own SO Question ---- TOOLTIP not to be added at the FIGURE Level. 
        #p = figure(tools="", background_fill_color="#efefef", x_range=cats,plot_width=195, plot_height=550,tooltips=TOOLTIPS)
        p = figure(tools="", background_fill_color="#efefef", x_range=cats,plot_width=625, plot_height=400)
        ## This -- plot_width=600, plot_height=550 --- INCLUDES the TOOLBAR on RIGHT .
        # This --  plot_height= 475 ---- If it goes above --- 475 cant see the X Scale. 
        from bokeh.models import HoverTool , WheelZoomTool , LassoSelectTool ,BoxZoomTool, ResetTool , PanTool
        b1 = p.vbar(cats, 0.7, q2[values_col], q3[values_col], fill_color="#E08E79", line_color="black")
        b2 = p.vbar(cats, 0.7, q1[values_col], q2[values_col], fill_color="#3B8686", line_color="black")
        b3 = p.rect(cats, lower[values_col], 0.2, 0.01,fill_color="blue", line_color="red") ## 
        b4 = p.rect(cats, upper[values_col], 0.2, 0.01, fill_color="blue", line_color="red") ## OK Own SO 

        hover = HoverTool(tooltips = TOOLTIPS, renderers = [b1, b2, b3,b4])
        p.add_tools(hover,WheelZoomTool(),LassoSelectTool(),BoxZoomTool(), ResetTool(),PanTool())

        # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        #[values_col]
        p.segment(cats, upper[values_col], cats, q3[values_col], line_color="black") #
        #p.segment(cats, lower.score, cats, q1.score, line_color="black")
        p.segment(cats, lower[values_col], cats, q1[values_col], line_color="black")
        #### BOKEH --- SEGMENT() -- The segment() function accepts start points x0, y0 and end points x1 and y1 
        # and renders segments between these
        # outliers
        if not out.empty:
            p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
            #print("----CIRCLE --------",p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6))
            ## Above == GlyphRenderer(id='

        p.xgrid.grid_line_color = "pink"
        #js_boxplot, div_boxplot = components(p) ## FOO_Error Experi 
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size="12pt"
        #p.toolbar.logo = None
        #p.toolbar_location = None
        js_boxplot, div_boxplot = components(p)
        cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 
        return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot

    def bokeh_tukey_summary_boxplot_large(self): #
        from bokeh.plotting import figure, show, output_file
        #from bokeh.charts import Area, show, output_file
        from bokeh.plotting import figure
        from bokeh.models import Range1d
        from bokeh.embed import components
        from bokeh.layouts import row

        df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
        
        #FOO_MAIN_GUESS the CATEGORICAL COLUMN  - Count Unique values in Each Column -- See which Column is categorical / Ordinal / Continous variable etc ...
        col_names_fromPSQL =  list(df_for_bokeh)
        #print("----Bokeh large BoxPlot-------col_names_fromPSQL------------",col_names_fromPSQL)
        ls_SeriesName = []
        ls_SeriesUnqCnts = [] 
        for k in range(len(col_names_fromPSQL)):
            series_name = str(col_names_fromPSQL[k])
            ls_SeriesName.append(series_name)
            unq_values_list = df_for_bokeh[series_name].unique()
            ls_SeriesUnqCnts.append(len(unq_values_list))
        df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts})
        min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']
        unq_values_list_final = df_for_bokeh[col_with_CategoricalValues].unique()

        groups = df_for_bokeh.groupby(str(col_with_CategoricalValues))
        q1 = groups.quantile(q=0.25) # print("-------------q1-----------------",q1) #
        ## Check if better way than QUANTILE to get QUANTILES  ## Should get QUANTILES same as SUMMARY Stats -UpperQ ,LowerQ== RStats  ?? 
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75) #print("-------------q3-----------------",q3)
        iqr = q3 - q1
        upper = q3 + 1.5*iqr #print("------------GROUPS ---- UPPER -------------",upper)
        lower = q1 - 1.5*iqr #print("------------GROUPS ---- LOWER -------------",lower)
        
        col_names_fromPSQL = list(df_for_bokeh) #
        ls_SeriesName = []
        ls_SeriesUnqCnts = [] 
        for k in range(len(col_names_fromPSQL)):
            series_name = str(col_names_fromPSQL[k])
            ls_SeriesName.append(series_name)
            unq_values_list = df_for_bokeh[series_name].unique() #print("---unq_values_list----",unq_values_list)
            ls_SeriesUnqCnts.append(len(unq_values_list))
        df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts}) #print(df_calcUnq)
        min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()  ## this -- min_valIndex --- is INDEX of SERIES with LEAST NUMBER of UNIQUE VALUES 
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']         #print(col_with_CategoricalValues)

        unq_values_list_final = df_for_bokeh[col_with_CategoricalValues].unique()
        #print("-------unq_values_list_final-------------",unq_values_list_final)
        # GET other 2 Column Names / Column Labels // Series Names --- which are NOT Categorical Variables
        list_of_other_Cols = []
        for k in range(len(col_names_fromPSQL)):
            if str(col_names_fromPSQL[k]) == col_with_CategoricalValues:
                pass
            else:
                list_of_other_Cols.append(str(col_names_fromPSQL[k]))
        #print("-----------list_of_other_Cols----------------",list_of_other_Cols)
        print("   "*90)

        # Get the UNIQUE Categories from SEGMENTS 
        ## col_with_CategoricalValues
        unq_segments_list = df_for_bokeh[col_with_CategoricalValues].unique() #


        # find the outliers for each category
        def outliers(group):
            #print("----------within_Function == OUTLIERS_group----------",group) 
            #print("---TYPE---within_Function == OUTLIERS_group----------",type(group))
            ## The CAT_A --- Grouped DF 

            # Get the UNIQUE Categories from SEGMENTS 
            ## col_with_CategoricalValues
            unq_segments_list = df_for_bokeh[col_with_CategoricalValues].unique() #
            values_col = list_of_other_Cols[0] #
            
            for k in range(len(unq_segments_list)): ## Getting only 2 categories --- may need a RANGE == LENgth + 1 etc .etc ..
                cat = unq_segments_list[k] #
            #     print("-----for LOOP ----group.name ==----cat________=========Within Func Outliers -------",cat)
            #     print("--------group.height > upper.loc[cat]['height']----------",group.height > upper.loc[cat][values_col])
            #     print("--------group.height < upper.loc[cat]['height']----------",group.height < upper.loc[cat][values_col])
            # #return group[(group.height > upper.loc[cat]['height']) | (group.height < lower.loc[cat]['height'])]['height']
            return group[(group[values_col] > upper.loc[cat][values_col])][values_col]
            # nuts = " "
            # return nuts
        out = groups.apply(outliers).dropna()
        #print("-------bokeh_large-----TYPE--out----------",type(out)) #OK# <class 'pandas.core.frame.DataFrame'>
        #print("-------bokeh_large-------out-----OUTLIERS from ALL Categories DataFrame---------",out) ## Can be EMPTY -- Empty DataFrame

        # prepare outlier data for plotting, we need coordinates for every outlier.
        if not out.empty:
            outx = []
            outy = []
            for keys in out.index:
                outx.append(keys[0])
                #print("-----bokeh_large----outx-----------",outx) 
                outy.append(out.loc[keys[0]].loc[keys[1]])
                #print("-----bokeh_large----outy-----------",outy) #
                # --------outx----------- ['CAT_C', 'CAT_C', 'CAT_C']
                # --------outy----------- [277.0, 355.0, 255.0]

        TOOLTIPS = """
            <div style="background-color:orange;">
                <div>
                    <span style="font-size: 15px; color: #966;">@cats</span>
                </div>
                
                <div>
                    <span style="font-size: 10px; color: black;">($y{int})</span>
                </div>
            </div>
        """                        

        # Get UNIQUE Categories --- CAT_A , CAT_B , CAT_C , from SEGMENTS 
        # The --- unq_segments_list --- defined above. 
        cats = unq_segments_list
        ## The --- list_of_other_Cols --- defined above. 
        values_col = list_of_other_Cols[0] #

        #p = figure(tools="", background_fill_color="#efefef", x_range=cats,plot_width=195, plot_height=550,tooltips=TOOLTIPS)
        ### As per Answer to Own SO Question ---- TOOLTIP not to be added at the FIGURE Level. 
        p = figure(tools="", background_fill_color="#efefef", x_range=cats,plot_width=625, plot_height=400)
        ## This -- plot_width=600, plot_height=550 --- INCLUDES the TOOLBAR on RIGHT .
        # This --  plot_height= 475 ---- If it goes above --- 475 cant see the X Scale. 
        from bokeh.models import HoverTool , WheelZoomTool , LassoSelectTool ,BoxZoomTool, ResetTool , PanTool
        b1 = p.vbar(cats, 0.7, q2[values_col], q3[values_col], fill_color="#E08E79", line_color="black")
        #print("-----------B1 ===========",b1)
        b2 = p.vbar(cats, 0.7, q1[values_col], q2[values_col], fill_color="#3B8686", line_color="black")
        #print("-----------B2 ===========",b2)
        #b3 = p.rect(cats, lower.height, 0.4, 0.15,angle=-0.7,fill_color="blue", line_color="pink") ## OK Experi with ANGLE  
        b3 = p.rect(cats, lower[values_col], 0.2, 0.01,fill_color="blue", line_color="red") ## 
        b4 = p.rect(cats, upper[values_col], 0.2, 0.01, fill_color="blue", line_color="red") ## OK Own SO 

        hover = HoverTool(tooltips = TOOLTIPS, renderers = [b1, b2, b3,b4])
        p.add_tools(hover,WheelZoomTool(),LassoSelectTool(),BoxZoomTool(), ResetTool(),PanTool())

        # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        #upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),upper.score)]
        
        # stems
        #[values_col]
        p.segment(cats, upper[values_col], cats, q3[values_col], line_color="black") #
        # # Ok Last Working Code --- 1400h_6MAY

        #p.segment(cats, lower.score, cats, q1.score, line_color="black")
        p.segment(cats, lower[values_col], cats, q1[values_col], line_color="black")
        # outliers
        if not out.empty:
            p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
            #print("----CIRCLE --------",p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6))
            ## Above == GlyphRenderer(id='

        p.xgrid.grid_line_color = "pink"
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size="12pt"

        #p.toolbar.logo = None
        #p.toolbar_location = None
        js_boxplot, div_boxplot = components(p)
        cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 
        
        return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot


    def bokeh_tukey_summary_boxplot_small(self): #
        from bokeh.plotting import figure, show, output_file
        from bokeh.plotting import figure
        from bokeh.models import Range1d
        from bokeh.embed import components
        from bokeh.layouts import row

        df_for_bokeh = pd.read_pickle("./df_holoviewPlots.pkl")
        ## Count Unique values in Each Column to see which Column is categorical / Ordinal / Continous variable etc ...
        col_names_fromPSQL =  list(df_for_bokeh)
        ls_SeriesName = []
        ls_SeriesUnqCnts = [] 
        for k in range(len(col_names_fromPSQL)):
            series_name = str(col_names_fromPSQL[k])
            ls_SeriesName.append(series_name)
            unq_values_list = df_for_bokeh[series_name].unique()
            ls_SeriesUnqCnts.append(len(unq_values_list))
        df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts})
        min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()
        ## Above == min_valIndex --- is the INDEX of the SERIES with LEAST NUMBER of UNIQUE VALUES 
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']
        unq_values_list_final = df_for_bokeh[col_with_CategoricalValues].unique()
        # GET other -- Column Names / Column Labels // Series Names --- which are NOT Categorical Variables
        list_of_other_Cols = []
        for k in range(len(col_names_fromPSQL)):
            if str(col_names_fromPSQL[k]) == col_with_CategoricalValues:
                pass
            else:
                list_of_other_Cols.append(str(col_names_fromPSQL[k]))

        # find the quartiles and IQR for each category
        groups = df_for_bokeh.groupby(str(col_with_CategoricalValues))
        # print("----------TYPE ---- groups----------",type(groups)) ## <class 'pandas.core.groupby.groupby.DataFrameGroupBy'>
        # print("------------------- groups----------",groups) ##  <pandas.core.groupby.groupby.DataFrameGroupBy object at 0x7f1fb59a0a58>
        #print("-==-DataFrameGroupBy object---- groups-----",groups.head())
        #for key, item in groups:  ### OK UNCOMMENT 
            #print(groups.get_group(key), "\n\n")
        #print("     "*90)
        q1 = groups.quantile(q=0.25)
        q2 = groups.quantile(q=0.5)
        q3 = groups.quantile(q=0.75)
        iqr = q3 - q1
        upper = q3 + 1.5*iqr
        lower = q1 - 1.5*iqr
        def outliers(group):
            # Get the UNIQUE Categories from SEGMENTS 
            unq_segments_list = df_for_bokeh[col_with_CategoricalValues].unique() #
            values_col = list_of_other_Cols[0] #
            values_col = str(values_col)
            for k in range(len(unq_segments_list)): ## Getting only 2 categories --- may need a RANGE == LENgth + 1 etc .etc ..
                cat = unq_segments_list[k] #
            #     print("-----for LOOP ----group.name ==----cat________=========Within Func Outliers -------",cat)
            #     print("--------group.height > upper.loc[cat]['height']----------",group.height > upper.loc[cat][values_col])
            #     print("--------group.height < upper.loc[cat]['height']----------",group.height < upper.loc[cat][values_col])
            # #return group[(group.height > upper.loc[cat]['height']) | (group.height < lower.loc[cat]['height'])]['height']
            #return group[(group.values_col > upper.loc[cat][values_col])][values_col]
        out = groups.apply(outliers).dropna()
        #print("-------bokeh_small-----TYPE--out----------",type(out)) #OK# <class 'pandas.core.frame.DataFrame'>
        #print("-------bokeh_small-------out-----OUTLIERS from ALL Categories DataFrame---------",out) ## Can be EMPTY -- Empty DataFrame

        # prepare outlier data for plotting, we need coordinates for every outlier.
        if not out.empty:
            outx = []
            outy = []
            for keys in out.index:
                outx.append(keys[0])
                outy.append(out.loc[keys[0]].loc[keys[1]])
        TOOLTIPS = """
            <div style="background-color:orange;">
                <div>
                    <span style="font-size: 15px; color: #966;">@cats</span>
                </div>
                
                <div>
                    <span style="font-size: 10px; color: black;">($y{int})</span>
                </div>
            </div>
        """                        

        unq_segments_list = df_for_bokeh['segments'].unique() #
        cats = unq_segments_list
        ### As per Answer to Own SO Question ---- TOOLTIP not to be added at the FIGURE Level. 
        p = figure(tools="", background_fill_color="#efefef", x_range=cats,plot_width=150, plot_height=170)
        from bokeh.models import HoverTool , WheelZoomTool , LassoSelectTool ,BoxZoomTool, ResetTool , PanTool
        b1 = p.vbar(cats, 0.7, q2.height, q3.height, fill_color="#E08E79", line_color="black")
        b2 = p.vbar(cats, 0.7, q1.height, q2.height, fill_color="#3B8686", line_color="black")
        b3 = p.rect(cats, lower.height, 0.2, 0.01,fill_color="blue", line_color="red") ## 
        b4 = p.rect(cats, upper.height, 0.2, 0.01, fill_color="blue", line_color="red") ## OK Own SO 

        hover = HoverTool(tooltips = TOOLTIPS, renderers = [b1, b2, b3,b4])
        p.add_tools(hover,WheelZoomTool(),LassoSelectTool(),BoxZoomTool(), ResetTool(),PanTool())

        # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        upper.height = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'height']),upper.height)]
        # print("-----TYPE===upper.score------",type(upper.height))# <class 'pandas.core.series.Series'>
        lower.height = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'height']),lower.height)]
        # stems
        p.segment(cats, upper.height, cats, q3.height, line_color="black") #
        # # Ok Last Working Code --- 1400h_6MAY
        p.segment(cats, lower.height, cats, q1.height, line_color="black")
        #### BOKEH --- SEGMENT() -- The segment() function accepts start points x0, y0 and end points x1 and y1 
        # and renders segments between these
        # outliers
        if not out.empty:
            p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
            #print("----CIRCLE --------",p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6))
            ## Above == GlyphRenderer(id='
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size="12pt"

        #print("--------------PLOT----BOKEH FINAL---------p----",p)
        
        #Own below here ______LOGO and TOOLBAR ok for BoxPlot _______________########

        p.toolbar.logo = None
        #p.toolbar_location = None
        
        js_boxplot, div_boxplot = components(p)
        cdn_js_boxplot=CDN.js_files[0] # NOT REQD ?? 
        cdn_css_boxplot=CDN.css_files[0] # NOT REQD ?? 
        
        return js_boxplot,div_boxplot ,cdn_js_boxplot,cdn_css_boxplot

        """
        ### Here ABOVE --- groups.apply(outliers)
        ### GROUPS ==  <class 'pandas.core.groupby.groupby.DataFrameGroupBy
        ## Source == https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.apply.html
        ## pandas.core.groupby.GroupBy.apply
        ## 
        The function passed to apply ----- in this case OUTLIERS ------ must take a dataframe as its first argument and 
        return a DataFrame, Series or scalar. 
        apply ---- will then take care of combining the results back together into a single dataframe or series. 
        apply ---- is therefore a highly flexible grouping method.
        """


        ##BELOW HERE ---- Own Old DC Pre SICK --- JAN2018 --- IRIS Scatter etc
        # ##### Bokeh Official Example - Area Chart
        
        
    def bokeh_scatter_iris(self): #
        from bokeh.plotting import figure, show, output_file
        #from bokeh.sampledata.iris import flowers
        from bokeh.models import ColumnDataSource, HoverTool
        import pandas as pd
        #from bokeh.charts import Area, show, output_file
        from bokeh.plotting import figure
        from bokeh.models import Range1d
        from bokeh.embed import components
        #from bkcharts import Area, show, output_file, defaults
        from bokeh.layouts import row
        
        
        #col_names_from_model = model_1b_col_names.objects.all().values('f1') 
        # 
        latest_dataSetName = temp_dataSetName_for_EDALanding.objects.all().values('dataset_name').order_by('-pk')[0:1]
        myDict_dataSetName = latest_dataSetName[0]
        for keys , values in myDict_dataSetName.items():
            if "dataset_name" in keys:
                dataset_name = str(values)
 
        from sqlalchemy import create_engine
       
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']
        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )
        engine = create_engine(database_url, echo=False)
        schema_default_public = "public"
        limit_records = 100 ## SCATTER TEST
        #
        sql_command = "SELECT * FROM {}.{} ;".format(str(schema_default_public), str(dataset_name),str(limit_records))
        df_for_scatterPlot = pd.read_sql(sql_command,engine)
        col_names_fromPSQL =  list(df_for_scatterPlot)
        #print("-----------col_names_fromPSQL------------",col_names_fromPSQL)
        #print("-----------dataset_name------FROM SCATTER FUNCTION -----------",dataset_name)
        # Count Unique values in Each Column to see which Column is categorical / Ordinal / Continous variable etc ...
        #
        #### Below Own Experi -- OK but Lists better for Comparison ?? 
        # dict_forcalc = {}
        # dict_forcalc['SeriesName'] = []
        # dict_forcalc['SeriesUnqCnts'] = []
        ls_SeriesName = []
        ls_SeriesUnqCnts = [] 
        for k in range(len(col_names_fromPSQL)):
            series_name = str(col_names_fromPSQL[k])
            #print(series_name)
            #dict_forcalc['SeriesName'].append(series_name)
            ls_SeriesName.append(series_name)
            unq_values_list = df_for_scatterPlot[series_name].unique()
            #print("----BOKEH SCATTER----unq_values_list--------",unq_values_list)
            #print(len(unq_values_list))
            #dict_forcalc['SeriesUnqCnts'].append(len(unq_cnt))
            ls_SeriesUnqCnts.append(len(unq_values_list))
        #print(dict_forcalc)
        df_calcUnq = pd.DataFrame({'ls_SeriesName':ls_SeriesName,'ls_SeriesUnqCnts':ls_SeriesUnqCnts})
        #print(df_calcUnq)
        #print("    "*90)
        min_valIndex = df_calcUnq['ls_SeriesUnqCnts'].idxmin()
        ## Above == min_valIndex --- is the INDEX of the SERIES with LEAST NUMBER of UNIQUE VALUES 
        col_with_CategoricalValues = df_calcUnq.iloc[min_valIndex]['ls_SeriesName']
        #print(col_with_CategoricalValues)
        #
        unq_values_list_final = df_for_scatterPlot[col_with_CategoricalValues].unique()
        #print("----------unq_values_list_final-------------",unq_values_list_final)
        #
        # GET other 2 Column Names / Column Labels // Series Names --- which are NOT Categorical Variables
        list_of_other_twoCols = []
        for k in range(len(col_names_fromPSQL)):
            if str(col_names_fromPSQL[k]) == col_with_CategoricalValues:
                pass
            else:
                list_of_other_twoCols.append(str(col_names_fromPSQL[k]))
        #print("-----------list_of_other_twoCols----------------",list_of_other_twoCols)
        #print("   "*90)



        
        ## Series from Col -1 
        #s1 = df_for_scatterPlot.iloc[:,0]
        #print("--------------Series ==1 -------------",s1) ## INDEX 
        #s2 = df_for_scatterPlot.iloc[:,1]
        #print("--------------Series ==2 -------------",s2) ##Col_1
        # s3 = df_for_scatterPlot.iloc[:,2]
        # s4 = df_for_scatterPlot.iloc[:,3]
        # s5 = df_for_scatterPlot.iloc[:,4]
        #print("---------------Series ==4 -------------",s4)
        #print("---------------Series ==5 -------------",s5)

        ########################### FOO--------------------- TBD --- According to this ------------------


        ##### FOO --- for actual scatter we need to pass in these SERIES from user 
        ##### user to choose WHICH COLUMNS --  on X Axis and Y Axis of scatter plot 

        #### User to pass in Input Param - stating - have 2 variables -- each variable in 1 Column 
        # then we do the following -- 
        # create a COLOR_MAP --- length_color_map == 2 * len(VAR_COLUMN)

        # series_len = s1.size
        # df_name_1 = pd.DataFrame() ## Empty DF 
        # df_name_2 = pd.DataFrame() ## Empty DF 
        # str_defaultFill = str(col_names_fromPSQL[0])   ## Height 
        # str_defaultFill_1 = str(col_names_fromPSQL[1]) ## Weight 
        # str_defaultFill_2 = str(col_names_fromPSQL[2]) ## Specimen
        # df_name_1['ColorMapBokeh'] = [str_defaultFill for x in np.arange(series_len)]
        # df_name_2['ColorMapBokeh'] = [str_defaultFill_1 for x in np.arange(series_len)]
        # df_for_concat = [df_name_1,df_name_2]
        # concat_df = pd.concat(df_for_concat)
        # series_for_concat = [s1,s2]
        # concat_series = pd.concat(series_for_concat)

        #print("------------df_name_1-----------------",df_name_1)
        #print("------------concat_df-----------------",concat_df)
        #print("--------concat_series-----------------",concat_series)
        #print("   "*90)
        #colormap = {}
        #
        d_colormap = dict.fromkeys(unq_values_list_final, 0)
        #print("---------d_colormap-------------",d_colormap)

        ## Above == {'Girl': 0, 'Man': 0, 'Boy': 0}
        ls_pallete_of_colors = ['red','blue','green','violet']

        for k in range(len(unq_values_list_final)):
            #
            #print(d_colormap[str(unq_values_list_final[k])])
            #
            d_colormap[unq_values_list_final[k]] = ls_pallete_of_colors[k]
            #
            #print(d_colormap[str(unq_values_list_final[k])])
        #print("-----------d_colormap--------------",d_colormap)

        # for k in range(len(unq_values_list)):
        #     #
        #     key_for_colormap = str(unq_values_list[k])
        #     colormap[]
        #colormap = {'Man': 'red', 'Boy': 'green', 'Girl': 'blue'} 
        ## Height -- RED ## Weight --- GREEN 
        #colors = [d_colormap[x] for x in df_for_scatterPlot['specimen']]
        #col_with_CategoricalValues
        colors = [d_colormap[x] for x in df_for_scatterPlot[col_with_CategoricalValues]]
        #print("----------colors-------------",colors)
        ### SO -- Source -- https://stackoverflow.com/questions/29517072/add-column-to-dataframe-with-default-value
       

        ##### FOO---- 
        # from bokeh.palettes import d3
        # from bokeh.sampledata.iris import flowers
        # print("--------------flowers------------------",flowers)
        # print("    "*90)

        # colormap = {'a': 'red', 'b': 'green'}
        # colors = [colormap[x] for x in flowers['species']]

        # #
        #colormap = {'col_1_int': 'red', 'col_2_int': 'green', 'col_4_int': 'blue'} #TBD_AUTOMATED_F5 from model 
        ### Need to get these Categorical Names STRINGS - Flower Types from DB 
        #colors = [colormap[x] for x in df_5_s]


        #print(len(colors))  ## this should be the LENGTH of the "Categorical Names" Column...

        #p = figure(title = "Iris Data - Bokeh Scatter Plot",plot_height=600,plot_width=900,tools="hover,crosshair,")

        names_of_variables = df_for_scatterPlot[col_with_CategoricalValues]

        TOOLTIPS = ("""

        <div>
                    <span style="font-size: 10px; color: black;">($x, $y)</span>
        </div>
        
                 """)

        # <div>

        #     <span style="font-size: 15px;">"VARIABLE_NAME"</span>
        #     <span style="font-size: 15px; color:blue;"> "@names_of_variables"</span>
        #     <br>
        #     <span style="font-size: 15px;"> "VARIABLE_VALUE" </span>
        #     <span style="font-size: 15px; color:red;"> "@df_5_l{}" </span>
        # </div>

        #p = figure(title = "Iris Data - Bokeh Scatter Plot",plot_height=550,plot_width=595,tooltips=TOOLTIPS)
        p = figure(plot_height=290,plot_width=220,tooltips=TOOLTIPS) ## No TITLE 
        # p.xaxis.axis_label = str(col_names_fromPSQL[0])
        # p.yaxis.axis_label = str(col_names_fromPSQL[1])
        if len(list_of_other_twoCols) == 1:
            #
            p.xaxis.axis_label = str(list_of_other_twoCols[0])
            p.yaxis.axis_label = str(list_of_other_twoCols[0])
            p.circle(df_for_scatterPlot[list_of_other_twoCols[0]],df_for_scatterPlot[list_of_other_twoCols[0]], color=colors, fill_alpha=0.2, size=10) ## TBD == color=colors,
        if len(list_of_other_twoCols) > 1:
            #
            p.xaxis.axis_label = str(list_of_other_twoCols[0])
            p.yaxis.axis_label = str(list_of_other_twoCols[1])
            p.circle(df_for_scatterPlot[list_of_other_twoCols[0]],df_for_scatterPlot[list_of_other_twoCols[1]], color=colors, fill_alpha=0.2, size=10) ## TBD == color=colors,
        


        
        # hover = HoverTool(tooltips="""
        # <div>
        #     <span style="font-size: 15px;">"VARIABLE_NAME"</span>
        #     <span style="font-size: 15px; color:blue;"> "@fruits"</span>
        #     <br>
        #     <span style="font-size: 15px;"> "VARIABLE_VALUE" </span>
        #     <span style="font-size: 15px; color:red;"> "@df_5_l{}" </span>
        # </div>
        
        #                            """)
        
        # hover_1 = HoverTool(tooltips=[
        #     ("VARIABLE_NAME", "@fruits"),
        #     ("VARIABLE_VALUE", "@df_1_s{(0.00 a)}"),  ## the "a" is required 
        #     ])
        
        # p.add_tools(hover)                  #####       ADD HOVER TOOL HERE 

        #p.circle(s4, s5, color=colors, fill_alpha=0.2, size=10)
        #p.circle(s1, s2, color=colors, fill_alpha=0.2, size=10) ## TBD == color=colors,
        #p.circle(df_for_scatterPlot[col_names_fromPSQL[0]],df_for_scatterPlot[col_names_fromPSQL[1]], color=colors, fill_alpha=0.2, size=10) ## TBD == color=colors,
        # list_of_other_twoCols
        
        
        
        #### BELOW FOO_ERROR --- FIX here below --- 
        #p.circle(df_for_scatterPlot[list_of_other_twoCols[0]],df_for_scatterPlot[list_of_other_twoCols[1]], color=colors, fill_alpha=0.2, size=10) ## TBD == color=colors,

        # BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths:: ('line_color', 198), ('x', 99), ('y', 99)
        # BokehUserWarning: ColumnDataSource's columns must be of the same length. Current lengths ('fill_color', 198), ('line_color', 198), ('x', 99), ('y', 99)
#        ## df_4_s == 1.8 --- Petal_Width
        p.toolbar.logo = None
        p.toolbar_location = None
       
        js, div = components(p,CDN)
        cdn_js=CDN.js_files[0]
        cdn_css=CDN.css_files[0]
        
        return js,div,cdn_js,cdn_css
    
        
    # GONE TO - dc_holoviews def bokeh_vbar_1(self):
    #     #
    #     from bokeh.io import show, output_file
    #     from bokeh.plotting import figure
    #     from bokeh.models import ColumnDataSource, HoverTool
    #     from bokeh.palettes import Spectral6
    #     from bokeh.resources import CDN
        
        
    #     #col_names_from_model = model_1b_col_names.objects.all().values('f1')  ##TBD__pass in colnames_model as a PARAMETER
    #     #ls_cols = list(col_names_from_model)
    #     #cols_list = [d['f1'] for d in ls_cols]

    #     ## PSQL to DF to Colum Names List 
    #     ## UNCOMMENT BELOW ---- Commented out as PSQL Flooded with Connections ...
    #     """
    #     from sqlalchemy import create_engine
    #     user = settings.DATABASES['default']['USER']
    #     password = settings.DATABASES['default']['PASSWORD']
    #     database_name = settings.DATABASES['default']['NAME']
    #     database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    #         user=user,
    #         password=password,
    #         database_name=database_name,
    #     )
    #     engine = create_engine(database_url, echo=False)
    #     schema_default_public = "public"
        
    #     """
    #     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    #     #p = figure(x_range=fruits, plot_width=100, plot_height=100,title="Fruit Counts")
    #     p = figure(x_range=fruits,plot_width=195, plot_height=150) ## Dont change
    #     ## This WIDTH and HEIGHT is PIXELS 
        
    #     p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)
    #     p.xgrid.grid_line_color = None
    #     p.y_range.start = 0
    #     p.toolbar.logo = None
    #     p.toolbar_location = None
    #     #show(p)
    #     #js_1, div_1 = components(p,CDN)
    #     js_1, div_1 = components(p)
    #     cdn_js=CDN.js_files[0] # NOT REQD ?? 
    #     cdn_css=CDN.css_files[0] # NOT REQD ?? 
    #     #print("--------cdn_css--------------",cdn_css)
    #     #print("--------cdn_js--------------",cdn_js)

        
    #     return js_1,div_1,cdn_js,cdn_css


