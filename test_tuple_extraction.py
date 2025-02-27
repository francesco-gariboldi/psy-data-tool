best_models=

if best_models.get('mixed_best_model'):
        mixed_best_formula = best_models['mixed_best_model']['formula']



non_mixed_best_model = (
    {
        'formula': 'ladder_score ~ freedom_to_make_life_choices + healthy_life_expectancy + regional_indicator + freedom_to_make_life_choices:healthy_life_expectancy',
        'aic': np.float64(251.67627681086788),
        'bic': np.float64(290.72757878815884),
        'r_squared': np.float64(0.7675720050765759),
        'adj_r_squared': np.float64(0.7470636525833325),
        'composite_score': np.float64(0.9668140986636276)
    },
    [
        np.float64(0.9474126707015018),
        np.float64(0.9436397349176624),
        np.float64(0.9668140986636276),
        np.float64(0.9571672150632589),
        np.float64(0.8927630766021022),
        np.float64(0.8907439964259047),
        np.float64(0.9239305392942208),
        np.float64(0.923930539294221),
        np.float64(0.8804358045548794),
        np.float64(0.9069457682298702),
        np.float64(0.9067131708364693),
        np.float64(0.8861147957570493),
        np.float64(0.8253367116125632),
        np.float64(0.8683120213497656),
        np.float64(0.816253323973916),
        np.float64(0.8146880865656245),
        np.float64(0.8146880865656245),
        np.float64(0.8008843292657658),
        np.float64(0.7349227297458678),
        np.float64(0.6997092983229468),
        np.float64(0.41501049661494727),
        np.float64(0.0)
    ]
)


mixed_best_model = (
    {
        'formula': (
            'ladder_score ~ freedom_to_make_life_choices + healthy_life_expectancy + '
            '(freedom_to_make_life_choices + healthy_life_expectancy | regional_indicator)'
        ),
        'aic': np.float64(275.1248819741877),
        'bic': np.float64(305.16434503364235),
        'marginal_r_squared': np.float64(0.7613937302199353),
        'conditional_r_squared': np.float64(0.6031037034920033),
        'composite_score': np.float64(0.8941013882741501)
    },
    [
        np.float64(0.8941013882741501),
        np.float64(0.7076768202736767),
        np.float64(0.8662779444471891),
        np.float64(0.8720302849544677),
        np.float64(0.8884344948895826),
        np.float64(0.8875525939746577),
        np.float64(0.7763773210289591),
        np.float64(0.7598608843539295),
        np.float64(0.46251582139258596),
        np.float64(0.8678097356241541),
        np.float64(0.8669079451076426),
        np.float64(0.7752331876982765),
        np.float64(0.756438148322926),
        np.float64(0.756114228674775),
        np.float64(0.874129173177729),
        np.float64(0.7565334243854577),
        np.float64(0.8684263735140234),
        np.float64(0.8673356786186549),
        np.float64(0.6142404441887391),
        np.float64(0.6692184904237202),
        np.float64(0.7135140512526091),
        np.float64(0.7833861866186583),
        np.float64(0.7614250089843533),
        np.float64(0.7815950101985405),
        np.float64(0.7595993729889489),
        np.float64(0.7795915035658947),
        np.float64(0.6434062148748119),
        np.float64(0.6601825327209838),
        np.float64(0.6303321961468813),
        np.float64(0.6296959722915932),
        np.float64(0.759325140789411),
        np.float64(0.7587199447728924),
        np.float64(0.7567435784610713),
        np.float64(0.7138623462727025),
        np.float64(0.712393274866953),
        np.float64(0.6007423683197465),
        np.float64(0.5646222810749268),
        np.float64(0.5591531086489988),
        np.float64(0.5662046063302405),
        np.float64(0.5598077616167167),
        np.float64(0.2870348648273904),
        np.float64(0.28651532233063026),
        np.float64(0.28139368509309576),
        np.float64(0.2520562520423287),
        np.float64(0.24999999988514)
    ]
)
