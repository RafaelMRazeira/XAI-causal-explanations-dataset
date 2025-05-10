import json
import threading
from tqdm import tqdm
from copy import copy
from loguru import logger
from openai import OpenAI


WHOLE_PROMPT = open("./data/prompt_example.txt", "r").read()

client = OpenAI()


def construct_whole_lawsuits(lawsuits):
    logger.info("Concatenando os processos para inferência.")
    whole_lawsuits = {}

    for k, v in lawsuits.items():
        whole_lawsuits_txt = ""

        for law_prog in v:
            whole_lawsuits_txt += f'{law_prog["Conteudo"]}\n'

        whole_lawsuits[k] = whole_lawsuits_txt

    return whole_lawsuits


def construct_gpt_messages(question, prompt):
    messages_gpt = [
        {
            "role": "system",
            "content": f"Você será apresentado a andamentos de processos públicos e seu trabalho é gerar um JSON como os exemplos abaixo. Sua resposta será apenas um JSON contendo as informações pedidas. Para o campo de 'Sentença' AS POSSÍVEIS TAGS são 'parcial', 'homologacao', 'procedente', 'improcedente', 'prejudicado', 'nulo', 'extinto', 'embargos rejeitados', 'deferido', 'indefiro', 'denegado', 'desistencia' e 'nao_classificado' e seu respectivo nó do grafo. O campo 'Edges_attr' POSSUI O MESMO TAMANHO QUE A QUANTIDADE DE NODES. USE OS EXEMPLOS ABAIXO PARA GERAR O JSON ESPERADO:\n    \n    {prompt}",
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    return messages_gpt


def process_whole_lawsuit(whole_lawsuits, lawsuit_number):
    message = construct_gpt_messages(whole_lawsuits.get(lawsuit_number), WHOLE_PROMPT)
    GPT_result = client.chat.completions.create(model="gpt-4o", messages=message)
    return lawsuit_number, GPT_result.choices[0].message.content


def set_last_progress_class_as_lawsuits_class(lawsuits):
    logger.info("Criando classes do processo como um todo.")
    LAWSUIT_CLASS = {}

    for lawsuit in tqdm(lawsuits.values()):
        for law_prog in lawsuit:
            if (
                law_prog["Classificacao"] != "nao_classificado"
            ):  # last sentence is the final classification
                LAWSUIT_CLASS[law_prog["Processo"]] = law_prog["Classificacao"]
                break

    return LAWSUIT_CLASS


def load_lawsuits():
    logger.info("Carregando processos.")
    autism_lawsuits = json.loads(
        f"{open('./data/sp_court_lawsuits.json.json', 'r').read()}"
    )
    return autism_lawsuits


def load_already_classified_lawsuits():
    try:
        logger.info("Verificando se existem processos já classificados...")
        already_classified_lawsuits = json.loads(
            f"{open('./data/already_classified_lawsuits.json', 'r').read()}"
        )
        logger.info(f"Achados {len(already_classified_lawsuits)} classificados.")

    except Exception as e:
        logger.info(f"Nenhum processo classificado foi achado.")
        already_classified_lawsuits = {}

    return already_classified_lawsuits


file_lock = threading.Lock()


def save_results_to_file(result):
    with file_lock:
        with open(
            "./data/already_classified_lawsuits.json",
            "w",
        ) as f:
            f.write(json.dumps(result, indent=4, ensure_ascii=False))


def classify_lawsuits_in_chat_gpt():
    logger.info("Iniciando classificação.")
    for lawsuit_number in tqdm(autism_lawsuits.keys(), position=0):
        _process_lawsuit(lawsuit_number)


def _run_whole_gpt(lawsuit_number):
    already_classified_lawsuits[lawsuit_number] = {}
    already_classified_lawsuits[lawsuit_number]["lawsuits"] = copy(
        autism_lawsuits[lawsuit_number]
    )

    _, GPT_whole_result = process_whole_lawsuit(whole_lawsuits, lawsuit_number)
    already_classified_lawsuits[lawsuit_number]["whole_gpt"] = GPT_whole_result
    already_classified_lawsuits[lawsuit_number]["whole_class"] = LAWSUITS_WHOLE_CLASSES[
        lawsuit_number
    ]
    save_results_to_file(already_classified_lawsuits)


def _process_lawsuit(lawsuit_number):
    if lawsuit_number in already_classified_lawsuits.keys():
        logger.info(f"Processo iniciado: {lawsuit_number}")
        logger.info(f"Verificando se já foi executado como um todo.")
        if "whole_gpt" not in already_classified_lawsuits[lawsuit_number]:
            logger.info(f"Processo não executado. Executando.")
            _run_whole_gpt(lawsuit_number)

        return
    _run_whole_gpt(lawsuit_number)


def classify_lawsuits_in_chat_gpt(autism_lawsuits):
    logger.info("Classificando processos com o ChatGPT.")
    for lawsuit_number in tqdm(autism_lawsuits.keys(), position=0):
        _process_lawsuit(lawsuit_number)


if __name__ == "__main__":
    autism_lawsuits = load_lawsuits()
    whole_lawsuits = construct_whole_lawsuits(autism_lawsuits)
    already_classified_lawsuits = load_already_classified_lawsuits()
    LAWSUITS_WHOLE_CLASSES = set_last_progress_class_as_lawsuits_class(autism_lawsuits)
    classify_lawsuits_in_chat_gpt(autism_lawsuits)
    logger.info("Processo finalizado com sucesso.")
