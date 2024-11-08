from shiny import App, reactive, render, ui
from faicons import icon_svg

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shinywidgets import output_widget, render_plotly

app_ui = ui.page_fluid(
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="https://static2.sharepointonline.com/files/fabric/office-ui-fabric-core/11.0.0/css/fabric.min.css"),
        ui.tags.style(
            """
            table {
                margin-bottom: 0px !important;
            }
            #best_model_rmse{
                font-size: 24.67px;
            }
            .custom-row {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 2%;
            }
            .custom-col {
                flex: 1;
                min-width: 20%;
                padding-top: 2px;
                padding-bottom: 2px;
                font-size: 0.8em;
            }
            .custom-col .shiny-input-select {
                height: 30px;
                font-size: 0.8em;
            }
            .modal-content {
                border-radius: 0px;
            }
            .modal-header, .modal-body, modal-footer {
                padding: 10px;
            }
            .modal-title {
                font-size: 18px;
            }
            .modal-footer .btn {
                padding: 10px;
                font-size: 13px;
                border-radius: 0px;
            }
            shiny-data-frame {
                font-size: 14px;
            }
            svg {
                margin: 0px !important;
            }
            body {
                background-color: rgb(183, 217, 255);
            }
            """
        )
    ),
    ui.div(
        class_ = "ms-Grid-row",
        style = "display: flex; flex-wrap: wrap; height:10px;"
    ),
    ui.div(
        ui.div(
            ui.div(
                ui.div("Upload", style = "font-size: 12.67px;"),
                ui.input_action_button(
                    "uploadButton",
                    "",
                    class_ = "btn-primary",
                    style = "height: 32px; padding: 0;",
                    icon = ui.tags.div(
                        icon_svg("upload"),
                        style="display: flex; align-items: center; justify-content: center;"
                    )
                ),
                ui.input_file("buttonUpload", "", accept=[".json"]),
                class_ = "card ms-depth-8",
                style = "padding: 22px; border-radius: 0px; height: 151px;"
            ),
            class_ = "ms-Grid-col ms-sm12 ms-lg6 ms-xl1"
        ),
        ui.div(
            class_ = "ms-Grid-col ms-sm12 ms-hiddenLgUp",
            style = "height:10px;"
            ),
        ui.div(
            ui.div(
                ui.div("Best model parameters:", style = "font-size: 12.67px;"),
                ui.output_data_frame("best_model_table"),
                class_ = "card ms-depth-8",
                style = "padding: 22px;  border-radius: 0px; height: 151px;"
            ),
            class_ = "ms-Grid-col ms-sm12 ms-lg6"
        ),
        ui.div(
            class_ = "ms-Grid-col ms-sm12 ms-lg12 ms-hiddenXlUp",
            style = "height:10px;"
            ),
        ui.div(
            ui.div(
                ui.div("Average RMSE", style = "font-size: 18px;"),
                ui.output_text(
                    "best_model_rmse"
                ),
                class_ = "card ms-depth-8",
                style = "padding: 22px; height: 95px;  border-radius: 0px; height: 151px;"
            ),
            class_ = "ms-Grid-col ms-sm12 ms-lg4 ms-xl2"
        ),
        ui.div(
            class_ = "ms-Grid-col ms-sm12 ms-hiddenLgUp",
            style = "height:10px;"
            ),
        ui.div(
            ui.div(
                ui.div("Modals:", style = "font-size: 12.67px;"),
                ui.tags.br(),
                ui.div(
                    ui.input_action_button(
                        "table_all_models",
                        "",
                        style = "height: 32px; padding: 0; border: none;",
                        class_ = "custom-col",
                        icon = icon_svg("table"),
                        title = "See a table of models results"
                    ),
                    ui.div(class_ = "custom-col"),
                    ui.input_action_button(
                        "heat_map",
                        "",
                        style = "height: 32px; padding: 0; border: none;",
                        class_ = "custom-col",
                        icon = icon_svg("grip"),
                        title = "See parameters heatmap"
                    ),
                    class_ = "custom-row"    
                ),                
                class_ = "card ms-depth-8",
                style = "padding: 22px; height: 95px; border-radius: 0px; height: 151px;"
            ),
            class_ = "ms-Grid-col ms-sm12 ms-lg4 ms-xl1"
        ),
        ui.div(
            class_ = "ms-Grid-col ms-sm12 ms-hiddenLgUp",
            style = "height:10px;"
            ),
        ui.div(
            ui.div(
                ui.tags.a(
                    ui.tags.img(
                        src = "https://raw.githubusercontent.com/davidrsch/LSTM_UTS/main/logo.png",
                        height = "95"
                    ),
                    href = ""
                ),
                class_ = "card ms-depth-8",
                style = "padding: 22px; height: 151px; display: flex; align-items: center; justify-content: center; border-radius: 0px;"
            ),
            class_ = "ms-Grid-col ms-sm12 ms-lg4 ms-xl2"
        ),
        class_ = "ms-Grid-row",
        style = "display: flex; flex-wrap: wrap;"
    ),
    ui.div(
        class_ = "ms-Grid-row",
        style = "display: flex; flex-wrap: wrap; height:10px;"
    ),
    ui.div(
        ui.div(
            ui.div(
                ui.div("Predictions behaviour:", style = "font-size:12.67px"),
                ui.div(
                    ui.div(
                        ui.input_select(
                            "transfo",
                            "Transformation",
                            choices = [], # This will be populated in server
                        ),
                    class_ = "custom-col"
                    ),
                    ui.div(
                        ui.input_select(
                            "scales",
                            "Scales",
                            choices = [],
                        ),
                        class_="custom-col"
                    ),
                    ui.div(
                        ui.input_select(
                            "inp_amount",
                            "Inputs",
                            choices = [],
                        ),
                        class_ = "custom-col"
                    ),
                    ui.div(
                        ui.input_select(
                            "lstm",
                            "LSTM",
                            choices = [],
                        ),
                        class_="custom-col"
                    ),
                    class_ = "custom-row"
                ),
                output_widget("predictions_plot"),
                class_ = "card ms-depth-8",
                style = "padding: 22px; border-radius: 0px;"
            ),
            class_ = "ms-Grid-col ms-lg12 ms-xl6"
        ),
        ui.div(
            class_ = "ms-Grid-col ms-lg12 ms-hiddenXlUp",
            style = "height:10px;"
            ),
        ui.div(
            ui.div(
                ui.div(
                    ui.div("RMSE by parameter:", style = "font-size:12.67px"),
                    ui.div(class_="custom-col"),
                    ui.div(
                        ui.input_select(
                            "parameter",
                            "Parameter:",
                            choices = ["transformations","scales","inp_amount","lstm"],
                        ),
                        class_="custom-col"
                    ),
                    class_ = "custom-row"
                ),
                output_widget("parameters_rmse"),
                class_ = "card ms-depth-8",
                style = "padding: 22px; border-radius: 0px;"
            ),
            class_ = "ms-Grid-col ms-lg12 ms-xl6"
        ),
        class_ = "ms-Grid-row",
        style = "display: flex; flex-wrap: wrap;"
    ),
    ui.tags.script(
        """
        $(document).on("click", "#uploadButton", function() {
            $("#buttonUpload").click();
        });
        """
    ),
    ui.tags.script(
        """
        const inputFile = document.querySelector('.form-group:has(#buttonUpload)');
        inputFile.style.display = 'none';
        """
    ) 
)

def server(input, output, session):
    file_data = reactive.Value(None)

    @reactive.Calc
    def best_model_json():
        file_info = input.buttonUpload()
        if file_info is not None and file_info[0]['datapath']:
            with open(file_info[0]['datapath'], 'r') as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                df = df.sort_values('rmse')
                columns_to_drop = ['horizon', 'epoch', 'tests_results']
                df = df[[col for col in df.columns if col not in columns_to_drop]]
                df = df.head(1)
                if 'transformations' in df.columns:
                    df = df.rename(columns={'transformations': 'tranfo'})
                return df
        return None

    @output
    @render.data_frame
    def best_model_table():
        data = best_model_json()
        if data is None:
            return None
        columns_to_drop = ['rmse']
        data = data[[col for col in data.columns if col not in columns_to_drop]]
        return render.DataGrid(data, filters=False)

    @output
    @render.text
    def best_model_rmse():
        data = best_model_json()
        if data is None:
            return "No data"
        return f"{data['rmse'].iloc[0]:.4f}"

    @reactive.Effect
    @reactive.event(input.buttonUpload)
    def _():
        file_info = input.buttonUpload()
        if file_info is not None and file_info[0]['datapath']:
            with open(file_info[0]['datapath'], 'r') as file:
                data = json.load(file)
                data = pd.DataFrame(data)
                file_data.set(data)
            best_data = best_model_json()

            unique_transfo = list(set(data['transformations']))
            ui.update_select("transfo", choices = unique_transfo)
            
            unique_scales = list(set(data['scales']))
            ui.update_select("scales", choices = unique_scales)

            unique_inp_amount = list(set(data['inp_amount']))
            ui.update_select("inp_amount", choices = unique_inp_amount)

            unique_lstm = list(set(data['lstm']))
            ui.update_select("lstm", choices = unique_lstm)

    @output
    @render_plotly
    def predictions_plot():
        if all(input[select_id]() for select_id in ["transfo", "scales", "inp_amount", "lstm"]):
            data = file_data()
            if data is None:
                return None

            df = pd.DataFrame(data)
            plot_data = df[
                (df['transformations'].astype(str) == input.transfo()) &
                (df['scales'].astype(str) == input.scales()) &
                (df['inp_amount'].astype(str) == input.inp_amount()) &
                (df['lstm'].astype(str) == input.lstm())
            ]
            
            test_results = pd.DataFrame(plot_data['tests_results'].iloc[0])
            test_cols = [col for col in test_results.columns if col.startswith('test_')]
            test_results['min'] = test_results[test_cols].min(axis=1)
            test_results['min_5'] = test_results[test_cols].quantile(0.05, axis=1)
            test_results['mean'] = test_results[test_cols].mean(axis=1)
            test_results['max_95'] = test_results[test_cols].quantile(0.95, axis=1)
            test_results['max'] = test_results[test_cols].max(axis=1)
            test_results['sd'] = test_results[test_cols].std(axis=1)

            fig = make_subplots(rows=2, cols=1, 
                       row_heights=[0.75, 0.25],
                       vertical_spacing=0.1)

            # Add fills between lines for uncertainty ranges
            fig.add_trace(
                go.Scatter(
                    x=test_results.index.tolist() + test_results.index.tolist()[::-1],
                    y=test_results['min'].tolist() + test_results['min_5'].tolist()[::-1],
                    fill='tonexty',
                    fillcolor='rgba(0,0,255,0.3)',
                    line=dict(width=0),
                    showlegend=False,
                    name='Min Range'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=test_results.index.tolist() + test_results.index.tolist()[::-1],
                    y=test_results['max'].tolist() + test_results['max_95'].tolist()[::-1],
                    fill='tonexty',
                    fillcolor='rgba(0,0,255,0.3)',
                    line=dict(width=0),
                    showlegend=False,
                    name='Max Range'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=test_results.index.tolist() + test_results.index.tolist()[::-1],
                    y=test_results['min_5'].tolist() + test_results['max_95'].tolist()[::-1],
                    fill='tonexty',
                    fillcolor='rgba(0,0,255,0.6)',
                    line=dict(width=0),
                    showlegend=False,
                    name='95% Range'
                ),
                row=1, col=1
            )

            # Add mean line
            fig.add_trace(
                go.Scatter(
                    x=test_results.index,
                    y=test_results['mean'],
                    line=dict(color='blue', dash='dash'),
                    name='Predicted (mean)'
                ),
                row=1, col=1
            )

            # Add boundary lines
            for col in ['max', 'min', 'max_95', 'min_5']:
                fig.add_trace(
                    go.Scatter(
                        x=test_results.index,
                        y=test_results[col],
                        line=dict(color='blue'),
                        showlegend=False if col not in ['min_5'] else True,
                        name='Predicted' if col == 'min_5' else col
                    ),
                    row=1, col=1
                )

            # Add real values
            fig.add_trace(
                go.Scatter(
                    x=test_results.index,
                    y=test_results['value'],
                    line=dict(color='green'),
                    opacity=0.5,
                    name='Real'
                ),
                row=1, col=1
            )

            # Add standard deviation plot
            fig.add_trace(
                go.Scatter(
                    x=test_results.index,
                    y=test_results['sd'],
                    line=dict(color='black'),
                    name='Predictions Standard deviation'
                ),
                row=2, col=1
            )

            # Update layout
            fig.update_layout(
                height=375,
                showlegend=True,
                yaxis1=dict(title='Predicted and Real values'),
                yaxis2=dict(title='SD'),
                xaxis2=dict(title='Sequence'),
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    tracegroupgap=5  # Add some gap between legend groups
                ),
                legend2=dict(
                    yanchor="top",
                    y=0.25,    # Position for the second legend
                    xanchor="right",
                    x=0.99
                )
            )

            # Update the SD trace to use the second legend
            fig.data[-1].update(legendgroup="group2", legend="legend2")

            return fig
        
    @output
    @render_plotly
    @reactive.Calc
    def parameters_rmse():
        if not input.parameter() or file_data() is None:
            return None

        data = file_data()
        df = pd.DataFrame(data)
        plot_data = df[[input.parameter(), 'rmse']]
        plot_data.columns = ['parameter', 'RMSE']
        
        fig = px.box(
            plot_data,
            x='parameter',
            y='RMSE',       
            title='RMSE by Parameter',  
        )
    
        # Customize axis labels
        fig.update_layout(
            xaxis_title=input.parameter(),  
            yaxis_title="RMSE"              
        )
        
        return fig

    @reactive.Effect
    @reactive.event(input.table_all_models)
    def all_models_modal():
        ui.modal_show(ui.modal(
            ui.output_data_frame("all_models_results"),
            title = "All Models Results",
            easy_close = True,
            size = "l",
            footer = ui.modal_button("Close")
        ))
    
    @output
    @render.data_frame
    def all_models_results():
        data = file_data()
        df = pd.DataFrame(data)
        table = df.drop(columns=['horizon', 'epoch', 'tests_results'])
        table = table.rename(columns={'transformations': 'tranfo'})
        return render.DataGrid(table, filters=True)

    @reactive.Effect
    @reactive.event(input.heat_map)
    def heat_map_modal():
        ui.modal_show(ui.modal(
            ui.div(
                ui.div("Select parameters:", style = "font-size:12.67px"),
                ui.div(class_ = "custom-col"),
                ui.div(
                    ui.input_select(
                        "x_axis",
                        "X_axis:",
                        choices = ["transformations","scales","inp_amount","lstm"],
                    ),
                    class_ = "custom-col",
                    style = "min-width: 140px"
                ),
                ui.div(
                    ui.input_select(
                        "y_axis",
                        "Y_axis:",
                        choices = ["transformations","scales","inp_amount","lstm"],
                    ),
                    class_ = "custom-col",
                    style = "min-width: 140px"
                ),
                class_ = "custom-row"
            ),
            ui.tags.br(),
            ui.output_plot("heat_map_plot"),
            title = "Heat map:",
            easy_close = True,
            size = "l",
            footer = ui.modal_button("Close")
        ))

    @output
    @render.plot
    def heat_map_plot():
        data = file_data()
        df = pd.DataFrame(data)
        
        if input.x_axis() == input.y_axis():
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Please select different axes", 
                    ha='center', va='center', fontsize=20)
            ax.axis('off')
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a pivot table for the heatmap
        pivot_table = pd.pivot_table(df, 
                                     values='rmse', 
                                     index=input.y_axis(), 
                                     columns=input.x_axis(), 
                                     aggfunc='first')
        
        # Create the heatmap with a blue color palette
        sns.heatmap(pivot_table, ax=ax, cmap='Blues', annot=True, fmt='.2f')
        
        ax.set_ylabel(input.y_axis())
        ax.set_xlabel(input.x_axis())
        ax.set_title('RMSE Heatmap')
        
        return fig

app = App(ui = app_ui, server = server)