import os
import rpy2
import r_warnings
from IPython.display import display
import IPython


# Plot best models diagnostics with plot() function
def plot_best_models_diagnostics(best_models, df_r):
    # Start by opening a PDF file
    r_code = """
    pdf(file="./rplots.pdf", width = 7, height = 56)
    """
    
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        non_mixed_best_formula = best_models['non_mixed_best_model'][0]['formula']
        r_non_mixed_best_formula = rpy2.robjects.StrVector([non_mixed_best_formula])
        rpy2.robjects.globalenv['non_mixed_best_formula'] = r_non_mixed_best_formula[0] 
        print(f"Non-mixed best model formula: {non_mixed_best_formula}")

        r_code += f"""
        non_mixed_best_model <- lm(non_mixed_best_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Diagnostic graphics for best non-mixed model
        plot(non_mixed_best_model, which=1, main=sprintf("Non-Mixed Model: %s - Residuals vs Fitted", non_mixed_best_formula))
        plot(non_mixed_best_model, which=2, main=sprintf("Non-Mixed Model: %s - Normal Q-Q", non_mixed_best_formula))
        plot(non_mixed_best_model, which=3, main=sprintf("Non-Mixed Model: %s - Scale-Location", non_mixed_best_formula))
        plot(non_mixed_best_model, which=5, main=sprintf("Non-Mixed Model: %s - Residuals vs Leverage", non_mixed_best_formula))
        """
    else:
        print("The best non-mixed model is missing or invalid.")

    # Plot for mixed model if available
    if best_models.get('mixed_best_model'):
        mixed_best_formula = best_models['mixed_best_model'][0]['formula']
        r_mixed_best_formula = rpy2.robjects.StrVector([mixed_best_formula])
        rpy2.robjects.globalenv['mixed_best_formula'] = r_mixed_best_formula[0]
        print(f"Mixed best model formula: {mixed_best_formula}")

        r_code += f"""
        mixed_best_model <- lmer(mixed_best_formula, data=df_r)

        par(mfrow=c(5,1))

        # Mixed Model diagnostic graphics using appropriate functions
        plot1 <- plot(fitted(mixed_best_model), resid(mixed_best_model), main=sprintf("Mixed Model: %s - Residuals vs Fitted", mixed_best_formula))
        plot2 <- qqnorm(resid(mixed_best_model), main=sprintf("Mixed Model: %s - Normal Q-Q", mixed_best_formula))
        plot3 <- qqline(resid(mixed_best_model))
        plot4 <- (fitted(mixed_best_model), sqrt(abs(resid(mixed_best_model))), main=sprintf("Mixed Model: %s - Scale-Location", mixed_best_formula))
        plot5 <- (hatvalues(mixed_best_model), resid(mixed_best_model), main=sprintf("Mixed Model: %s - Residuals vs Leverage", mixed_best_formula))

        # Arrange the plots in a 5x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, plot5, ncol=1)
        """
    else:
        print("The best mixed model is missing or invalid.")
    
    # Close the PDF file
    r_code += """
    dev.off()
    """
    
    try:
        # Execute the R code to generate the PDF
        rpy2.robjects.r(r_code)

        # Verify that the PDF was created
        pdf_path = './rplots.pdf'
        if os.path.exists(pdf_path):
            print(f"PDF generated successfully: {pdf_path}")
            
            # Display the PDF file in the Jupyter notebook
            display(IPython.display.IFrame(pdf_path, width=800, height=600))
        else:
            print("PDF file was not generated.")

    except Exception as e:
        print("Error encountered while generating plots:", e)
        r_warnings.print_r_warnings()


# Plot best models diagnostics with ggplot2() function
def plot_best_models_diagnostics_ggplot2(best_models, df_r):
    # Start by opening a PDF file
    r_code = """
    pdf(file="./rplots.pdf", width = 10, height = 35)
    """
    
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        # Retrieve the formula for the non-mixed model (Python string)
        non_mixed_best_formula = best_models['non_mixed_best_model'][0]['formula']
        # Convert the formula to an R string and assign it to the R
        # environment
        r_non_mixed_best_formula = rpy2.robjects.StrVector([non_mixed_best_formula])
        rpy2.robjects.globalenv['non_mixed_best_formula'] = r_non_mixed_best_formula[0] 
        print(f"Non-mixed best model formula: {non_mixed_best_formula}")

        r_code += f"""
        non_mixed_best_model <- lm(non_mixed_best_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Residuals vs. Fitted plot directly in Jupyter with gglm()
        plot1 <- ggplot(data = non_mixed_best_model) +
                    stat_fitted_resid() +
                    labs(title = sprintf("Residuals vs. Fitted values for the non-mixed model:\n%s",
                                        paste(deparse(formula(non_mixed_best_model)), collapse = "")))


        # Normal Q-Q plot
        plot2 <- ggplot(data = non_mixed_best_model) +
                    stat_normal_qq() +
                    labs(title = sprintf("Normall Q-Q for the non-mixed model:\n%s",
                                        paste(deparse(formula(non_mixed_best_model)), collapse = "")))


        # Scale location diagnostic plot
        plot3 <- ggplot(data = non_mixed_best_model) +
                       stat_scale_location(
                       alpha = 0.5,
                       na.rm = TRUE,
                       se = TRUE,
                       method = "loess",
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Scale location (Residuals vs Fitted) values for the non-mixed model:\n%s",
                                           paste(deparse(formula(non_mixed_best_model)), collapse = "")))


        # Residual vs. leverage plot.
        plot4 <- ggplot(data = non_mixed_best_model) +
                       stat_resid_leverage(
                       alpha = 0.5,
                       method = "loess",
                       se = TRUE,
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Residual vs. Leverage values for the non-mixed model:\n%s",
                                           paste(deparse(formula(non_mixed_best_model)), collapse = "")))                                   

        # Arrange the plots in a 4x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, ncol=1)
        """
    else:
        print("The best non-mixed model is missing or invalid.")

    # Plot for mixed model if available
    if best_models.get('mixed_best_model'):
        mixed_best_formula = best_models['mixed_best_model'][0]['formula']
        r_mixed_best_formula = rpy2.robjects.StrVector([mixed_best_formula])
        rpy2.robjects.globalenv['mixed_best_formula'] = r_mixed_best_formula[0]
        print(f"Mixed best model formula: {mixed_best_formula}")

        r_code += f"""
        mixed_best_model <- lmer(mixed_best_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Residuals vs. Fitted plot directly in Jupyter with gglm()
        plot1 <- ggplot(data = mixed_best_model) +
                    stat_fitted_resid() +
                    labs(title = sprintf("Residuals vs. Fitted values for the mixed model:\n%s",
                                        paste(deparse(formula(mixed_best_model)), collapse = "")))


        # Normal Q-Q plot
        plot2 <- ggplot(data = mixed_best_model) +
                    stat_normal_qq() +
                    labs(title = sprintf("Normall Q-Q for the mixed model:\n%s",
                                        paste(deparse(formula(mixed_best_model)), collapse = "")))


        # Scale location diagnostic plot
        plot3 <- ggplot(data = mixed_best_model) +
                       stat_scale_location(
                       alpha = 0.5,
                       na.rm = TRUE,
                       se = TRUE,
                       method = "loess",
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Scale location (Residuals vs Fitted) values for the mixed model:\n%s",
                                           paste(deparse(formula(mixed_best_model)), collapse = "")))


        # Residual vs. leverage plot.
        plot4 <- ggplot(data = mixed_best_model) +
              stat_resid_leverage(
              alpha = 0.5,
              method = "loess",
              se = TRUE,
              color = "steelblue",
              ) +
              labs(title = sprintf("Residual vs. Leverage values for the mixed model:\n%s",
                                  paste(deparse(formula(mixed_best_model)), collapse = "")))                                   

        # Arrange the plots in a 4x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, ncol=1)
        """
    else:
        print("The best mixed model is missing or invalid.")
    
    # Close the PDF file
    r_code += """
    dev.off()
    """
    
    try:
        # Execute the R code to generate the PDF
        rpy2.robjects.r(r_code)

        # Verify that the PDF was created
        pdf_path = './rplots.pdf'
        if os.path.exists(pdf_path):
            print(f"PDF generated successfully: {pdf_path}")
            
            # Display the PDF file in the Jupyter notebook
            display(IPython.display.IFrame(pdf_path, width=800, height=600))
        else:
            print("PDF file was not generated.")

    except Exception as e:
        print("Error encountered while generating plots:", e)
        r_warnings.print_r_warnings()


# Scatterplot of the relation between two variables
def scatterplot(df_r, response_var, predictor_vars):
    # Convert the Pandas DataFrame to an R DataFrame
    r_df = rpy2.robjects.pandas2ri.py2rpy(df_r)
    rpy2.robjects.globalenv['r_df'] = r_df  # Assign to R environment

    # Prepare the R code for plotting
    r_code = """
    library(ggplot2)
    library(gridExtra)
    pdf(file="./model_plot.pdf", width = 10, height = 17)
    """

    if len(predictor_vars) == 1:
        # Case with one predictor variable
        r_code += f"""
        plot_data <- data.frame(
            {response_var} = r_df${response_var},
            {predictor_vars[0]} = r_df${predictor_vars[0]}
        )

        plot1 <- ggplot(plot_data, aes(x={predictor_vars[0]}, y={response_var})) +
                    geom_point() +
                    geom_smooth() +
                    labs(title = "Relation between {predictor_vars[0]} and {response_var}", 
                         x = "{predictor_vars[0]}", 
                         y = "{response_var}") +
                    theme_minimal()

        grid.arrange(plot1, ncol=1)
        """
    elif len(predictor_vars) == 2:
        # Case with two predictor variables
        r_code += f"""
        plot_data <- data.frame(
            {response_var} = r_df${response_var},
            {predictor_vars[0]} = r_df${predictor_vars[0]},
            {predictor_vars[1]} = r_df${predictor_vars[1]}
        )

        plot1 <- ggplot(plot_data, aes(x={predictor_vars[0]}, y={response_var})) +
                    geom_point() +
                    geom_smooth() +
                    labs(title = "Relation between {predictor_vars[0]} and {response_var}", 
                         x = "{predictor_vars[0]}", 
                         y = "{response_var}") +
                    theme_minimal()

        plot2 <- ggplot(plot_data, aes(x={predictor_vars[0]}, y={response_var}, color = {predictor_vars[1]})) +
                    geom_point() +
                    geom_smooth() +
                    labs(title = "Relation between {predictor_vars[0]} and {response_var}", 
                         x = "{predictor_vars[0]}", 
                         y = "{response_var}") +
                    theme_minimal()

        grid.arrange(plot1, plot2, ncol=1)
        """
    else:
        print("Invalid number of predictor variables provided. The function supports up to 2 predictor variables.")

    r_code += "dev.off()"

    try:
        # Execute the R code to generate the PDF
        rpy2.robjects.r(r_code)
        print("R code executed successfully.")

        # Verify that the PDF was created
        pdf_path = './model_plot.pdf'
        if os.path.exists(pdf_path):
            print(f"PDF generated successfully: {pdf_path}")
            
            # Display the PDF file in the Jupyter notebook
            IPython.display.display(IPython.display.IFrame(pdf_path, width=800, height=600))
        else:
            print("PDF file was not generated.")

    except Exception as e:
        print("Error encountered while generating plots:", e)


# Dynamic scatterplot of the relation between two variables
def dynamic_scatterplot(df_r, response_var, predictor_vars):
    # Convert the Pandas DataFrame to an R DataFrame
    rpy2.robjects.pandas2ri.activate()
    r_df = rpy2.robjects.pandas2ri.py2rpy(df_r)
    rpy2.robjects.globalenv['r_df'] = r_df  # Assign to R environment

    # Start R code for plotting
    r_code = """
    library(ggplot2)
    library(gridExtra)
    pdf(file="./model_plot.pdf", width = 10, height = 17)
    plot_list <- list()
    """
    
    # Iterate over predictor variables and create a plot for each
    for i, predictor_var in enumerate(predictor_vars):
        r_code += f"""
        # Check if the predictor variable is a factor
        if (is.factor(r_df${predictor_var})) {{
            plot_data_{i} <- data.frame(
                {response_var} = r_df${response_var},
                {predictor_var} = r_df${predictor_var}
            )
            
            plot{i+1} <- ggplot(plot_data_{i}, aes(x={predictor_var}, y={response_var}, color={predictor_var})) +
                         geom_point(position=position_jitter(width=0.2, height=0), alpha=0.7) +
                         geom_smooth(method="lm", se=FALSE) +
                         labs(title = "Relation between {predictor_var} (Factor) and {response_var}", 
                              x = "{predictor_var}",
                              y = "{response_var}") +
                         theme_minimal()
        
        }} else {{
            plot_data_{i} <- data.frame(
                {response_var} = r_df${response_var},
                {predictor_var} = r_df${predictor_var}
            )
            
            plot{i+1} <- ggplot(plot_data_{i}, aes(x={predictor_var}, y={response_var}, color={predictor_var})) +
                         geom_point(color="#2f3b86ff") +
                         geom_smooth(method="lm", color="#6327b3ff", fill="#5e9185ff") +
                         labs(title = "Relation between {predictor_var} and {response_var}", 
                              x = "{predictor_var}", 
                              y = "{response_var}") +
                         theme(panel.background = element_rect(fill = '#e2dfd8ff', colour = '#2f3b86ff'))
        }}
        
        plot_list[[{i+1}]] <- plot{i+1}
        """

    # Arrange all plots in a grid
    r_code += """
    do.call(grid.arrange, c(plot_list, ncol=1))
    dev.off()
    """

    try:
        # Execute the R code to generate the PDF
        rpy2.robjects.r(r_code)
        print("R code executed successfully.")

        # Verify that the PDF was created
        pdf_path = './model_plot.pdf'
        if (os.path.exists(pdf_path)):
            print(f"PDF generated successfully: {pdf_path}")
            
            # Display the PDF file in the Jupyter notebook
            IPython.display.display(IPython.display.IFrame(pdf_path, width=800, height=600))
        else:
            print("PDF file was not generated.")

    except Exception as e:
        print("Error encountered while generating plots:", e)
