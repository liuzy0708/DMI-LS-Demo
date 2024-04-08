import shap
from Def_DMI_DD import DMI_DD_strategy
from clf_BLS_SMW import BLS
from skmultiflow.data import SEAGenerator
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings("ignore")


shap.initjs()

stream = SEAGenerator(random_state=1)
X_pt, y_pt = stream.next_sample(100)

n_class = stream.n_classes
chunk_size = 100
max_samples = 10000
count = 0
query_size = 10
state_count = 0

model_SHAP_BLS = BLS(Nf=10,
                 Ne=10,
                 N1=10,
                 N2=10,
                 map_function='sigmoid',
                 enhence_function='sigmoid',
                 reg=0.001)

model_SHAP_BLS.fit(X_pt, y_pt)

y_pred = []
y_true = []

strategy = DMI_DD_strategy(n_class, model_SHAP_BLS, X_pt, chunk_size=chunk_size, query_size=query_size)

while count < max_samples and stream.has_more_samples():
    X_chunk_t, y_chunk_t = stream.next_sample(chunk_size)
    y_pred = y_pred + model_SHAP_BLS.predict(X_chunk_t).tolist()
    y_true = y_true + y_chunk_t.tolist()

    model_SHAP_BLS = strategy.evaluation(X_chunk_t, y_chunk_t, clf=model_SHAP_BLS)

    count += chunk_size
    state_count += chunk_size
    if state_count % (max_samples * 3 * 0.10) == 0:
        print('\nHave processed {:.0f}%'.format(state_count / (max_samples * 3) * 100), 'samples\n')

    acc_SHAP_BLS = accuracy_score(y_pred, y_true)
    print(acc_SHAP_BLS)