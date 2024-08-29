import os
import rpy2
import r_warnings
import IPython


# Plot best models diagnostics with plot() function
def plot_best_models_diagnostics(best_models, df_r):
    # Start by opening a PDF file
    r_code = """
    pdf(file="./rplots.pdf", width = 7, height = 56)
    """
    
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        non_mixed_formula = best_models['non_mixed_best_model']['formula']
        r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
        rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0] 
        print(f"Non-mixed model formula: {non_mixed_formula}")

        r_code += f"""
        non_mixed_model <- lm(non_mixed_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Diagnostic graphics for best non-mixed model
        plot(non_mixed_model, which=1, main=sprintf("Non-Mixed Model: %s - Residuals vs Fitted", non_mixed_formula))
        plot(non_mixed_model, which=2, main=sprintf("Non-Mixed Model: %s - Normal Q-Q", non_mixed_formula))
        plot(non_mixed_model, which=3, main=sprintf("Non-Mixed Model: %s - Scale-Location", non_mixed_formula))
        plot(non_mixed_model, which=5, main=sprintf("Non-Mixed Model: %s - Residuals vs Leverage", non_mixed_formula))
        """
    else:
        print("Non-mixed best model is missing or invalid.")

    # Plot for mixed model if available
    if best_models.get('mixed_best_model'):
        mixed_formula = best_models['mixed_best_model']['formula']
        r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])
        rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]
        print(f"Mixed model formula: {mixed_formula}")

        r_code += f"""
        mixed_model <- lmer(mixed_formula, data=df_r)

        par(mfrow=c(5,1))

        # Mixed Model diagnostic graphics using appropriate functions
        plot1 <- plot(fitted(mixed_model), resid(mixed_model), main=sprintf("Mixed Model: %s - Residuals vs Fitted", mixed_formula))
        plot2 <- qqnorm(resid(mixed_model), main=sprintf("Mixed Model: %s - Normal Q-Q", mixed_formula))
        plot3 <- qqline(resid(mixed_model))
        plot4 <- (fitted(mixed_model), sqrt(abs(resid(mixed_model))), main=sprintf("Mixed Model: %s - Scale-Location", mixed_formula))
        plot5 <- (hatvalues(mixed_model), resid(mixed_model), main=sprintf("Mixed Model: %s - Residuals vs Leverage", mixed_formula))

        # Arrange the plots in a 5x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, plot5, ncol=1)
        """
    else:
        print("Mixed best model is missing or invalid.")
    
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


# Plot best models diagnostics with gglm() function
def plot_best_models_diagnostics_gglm(best_models, df_r):
    # Start by opening a PDF file
    r_code = """
    pdf(file="./rplots.pdf", width = 7, height = 56)
    par(mfrow=c(8,1))
    """
    
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        non_mixed_formula = best_models['non_mixed_best_model']['formula']
        r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
        rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0] 
        print(f"Non-mixed model formula: {non_mixed_formula}")

        r_code += f"""
        non_mixed_model <- lm(non_mixed_formula, data=df_r)
        
        # Diagnostic graphics for best non mixed model using gglm
        gglm(non_mixed_model)
        """
    else:
        print("Non-mixed best model is missing or invalid.")

    # Plot for mixed model if available
    if best_models.get('mixed_best_model'):
        mixed_formula = best_models['mixed_best_model']['formula']
        r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])
        rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]
        print(f"Mixed model formula: {mixed_formula}")

        r_code += f"""
        mixed_model <- lmer(mixed_formula, data=df_r)
        
        # Assuming gglm(non_mixed_model) generates one plot, replicate this for four different diagnostics
        plot1 <- gglm(non_mixed_model, which=1) # Residuals vs Fitted
        plot2 <- gglm(non_mixed_model, which=2) # Normal Q-Q
        plot3 <- gglm(non_mixed_model, which=3) # Scale-Location
        plot4 <- gglm(non_mixed_model, which=4) # Cook's distance

        # Arrange the plots in a 4x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, ncol=1)
        """
    else:
        print("Mixed best model is missing or invalid.")
    
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
    pdf(file="./rplots.pdf", width = 7, height = 56)
    """
    
    # Plot for non-mixed model if available
    if best_models.get('non_mixed_best_model'):
        non_mixed_formula = best_models['non_mixed_best_model']['formula']
        r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
        rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0] 
        print(f"Non-mixed model formula: {non_mixed_formula}")

        r_code += f"""
        non_mixed_model <- lm(non_mixed_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Residuals vs. Fitted plot directly in Jupyter with gglm()
        plot1 <- ggplot(data = non_mixed_model) +
                    stat_fitted_resid() +
                    labs(title = sprintf("Residuals vs. Fitted values for the non-mixed model:\n%s",
                                        paste(deparse(formula(non_mixed_model)), collapse = "")))


        # Normal Q-Q plot
        plot2 <- ggplot(data = non_mixed_model) +
                    stat_normal_qq() +
                    labs(title = sprintf("Normall Q-Q for the non-mixed model:\n%s",
                                        paste(deparse(formula(non_mixed_model)), collapse = "")))


        # Scale location diagnostic plot
        plot3 <- ggplot(data = non_mixed_model) +
                       stat_scale_location(
                       alpha = 0.5,
                       na.rm = TRUE,
                       se = TRUE,
                       method = "loess",
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Scale location (Residuals vs Fitted) values for the non-mixed model:\n%s",
                                           paste(deparse(formula(non_mixed_model)), collapse = "")))


        # Residual vs. leverage plot.
        plot4 <- ggplot(data = non_mixed_model) +
                       stat_resid_leverage(
                       alpha = 0.5,
                       method = "loess",
                       se = TRUE,
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Residual vs. Leverage values for the non-mixed model:\n%s",
                                           paste(deparse(formula(non_mixed_model)), collapse = "")))                                   

        # Arrange the plots in a 4x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, ncol=1)
        """
    else:
        print("Non-mixed best model is missing or invalid.")

    # Plot for mixed model if available
    if best_models.get('mixed_best_model'):
        mixed_formula = best_models['mixed_best_model']['formula']
        r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])
        rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]
        print(f"Mixed model formula: {mixed_formula}")

        r_code += f"""
        mixed_model <- lmer(mixed_formula, data=df_r)
        
        par(mfrow=c(4,1))

        # Residuals vs. Fitted plot directly in Jupyter with gglm()
        plot1 <- ggplot(data = mixed_model) +
                    stat_fitted_resid() +
                    labs(title = sprintf("Residuals vs. Fitted values for the mixed model:\n%s",
                                        paste(deparse(formula(mixed_model)), collapse = "")))


        # Normal Q-Q plot
        plot2 <- ggplot(data = mixed_model) +
                    stat_normal_qq() +
                    labs(title = sprintf("Normall Q-Q for the mixed model:\n%s",
                                        paste(deparse(formula(mixed_model)), collapse = "")))


        # Scale location diagnostic plot
        plot3 <- ggplot(data = mixed_model) +
                       stat_scale_location(
                       alpha = 0.5,
                       na.rm = TRUE,
                       se = TRUE,
                       method = "loess",
                       color = "steelblue",
                       ) +
                       labs(title = sprintf("Scale location (Residuals vs Fitted) values for the mixed model:\n%s",
                                           paste(deparse(formula(mixed_model)), collapse = "")))


        # Residual vs. leverage plot.
        plot4 <- ggplot(data = mixed_model) +
              stat_resid_leverage(
              alpha = 0.5,
              method = "loess",
              se = TRUE,
              color = "steelblue",
              ) +
              labs(title = sprintf("Residual vs. Leverage values for the mixed model:\n%s",
                                  paste(deparse(formula(mixed_model)), collapse = "")))                                   

        # Arrange the plots in a 4x1 grid
        grid.arrange(plot1, plot2, plot3, plot4, ncol=1)
        """
    else:
        print("Mixed best model is missing or invalid.")
    
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
