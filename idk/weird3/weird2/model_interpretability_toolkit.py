import shap
import lime
import lime.lime_tabular

class ModelInterpretabilityToolkit:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.Explainer(model)
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=None,
            feature_names=feature_names,
            class_names=['output'],
            mode='regression'
        )

    def get_shap_values(self, data):
        return self.explainer(data)

    def plot_shap_summary(self, data):
        shap_values = self.get_shap_values(data)
        shap.summary_plot(shap_values, data, feature_names=self.feature_names)

    def get_lime_explanation(self, instance):
        exp = self.lime_explainer.explain_instance(
            instance, 
            self.model.predict, 
            num_features=len(self.feature_names)
        )
        return exp

    def plot_lime_explanation(self, instance):
        exp = self.get_lime_explanation(instance)
        exp.as_pyplot_figure()

    def get_feature_importance(self, data):
        shap_values = self.get_shap_values(data)
        return dict(zip(self.feature_names, np.abs(shap_values.values).mean(0)))

interpretability_toolkit = ModelInterpretabilityToolkit(model=some_model, feature_names=['feature1', 'feature2', ...])
