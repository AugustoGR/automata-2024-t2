"""Implementação de autômatos finitos."""


def load_automata(filename):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estsrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

    Um exemplo de arquivo válido é:

    ```
    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2
    ```

    Caso o arquivo seja inválido uma exceção Exception é gerada.

    """

    with open(filename, "rt", encoding="utf-8") as arquivo:
        # processa arquivo...
        alphabet = tuple(arquivo.readline().strip().split())
        states = tuple(arquivo.readline().strip().split())
        final_states = tuple(arquivo.readline().strip().split())
        initial_state = arquivo.readline().strip()
        delta = []
        for line in arquivo:
            temp_edge = tuple(line.strip().split())
            delta.append(temp_edge)

    if initial_state not in states:
        raise ValueError("invalid initial state")

    for state in final_states:
        if state not in states:
            raise ValueError("invalid final state")

    for edge in delta:
        if not (
            edge[0] in states and 
            ( edge[1] in alphabet or edge[1] == '&') and 
            edge[2] in states
        ):
            raise ValueError("invalid edge")

    return (states, alphabet, delta, initial_state, final_states)


def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """

    delta = automata[0]
    alphabet = automata[1]
    delta = automata[2]
    initial_state = automata[3]
    final_states = automata[4]
    result = {}
    for word in words:
        current_state = initial_state
        is_valid_word = True
        for symbol in word:
            if symbol not in alphabet:
                result[word] = "INVALIDA"
                is_valid_word = False
                break
            for edge in delta:
                if edge[0] == current_state and edge[1] == symbol:
                    current_state = edge[2]
                    break
        if is_valid_word:
            if current_state in final_states:
                result[word] = "ACEITA"
            else:
                result[word] = "REJEITA"

    return result

def handle_closure(state, delta):
    """Retorna o fecho de um estado em um NFA."""
    closure = {state}
    stack = [state]

    while stack:
        current = stack.pop()
        for edge in delta:
            if edge[0] == current and edge[1] == '&' and edge[2] not in closure:
                closure.add(edge[2])
                stack.append(edge[2])
    
    return closure

def convert_to_dfa(automata):
    """Converte um NFA num DFA."""
    alphabet = automata[1]
    delta = automata[2]
    initial_state = automata[3]
    final_states = automata[4]

    new_states = []
    new_delta = []
    new_final_states = []
    new_initial_state = initial_state
    
    initial_closure = handle_closure(initial_state, delta)
    queue = [initial_closure]
    watched = []
    while queue:
        current = queue.pop()
        new_states.append(current)
        
        for symbol in alphabet:
            new_state = set()
            for state in current:
                for edge in delta:
                    if edge[0] == state and edge[1] == symbol:
                        new_state = new_state.union(
                            handle_closure(edge[2], delta)
                        )
            if new_state:
                new_delta.append((current, symbol, new_state))
                if new_state not in watched:
                    watched.append(new_state)
                    queue.append(new_state)

    # Atualiza estados finais
    for new_state in new_states:
        for state in new_state:
            if state in final_states:
                new_final_states.append(new_state)
                break
    
    # Atualiza estado inicial
    for new_state in new_states:
        if initial_state in new_state:
            new_initial_state = new_state
            break

    # Formatação dos dados
    temp_new_state = []
    for new_state in new_states:
        temp_new_state = ''.join(new_state)
    new_states = temp_new_state

    temp_new_delta = []
    for edge in new_delta:
        temp_org = ''.join(edge[0])
        temp_dest = ''.join(edge[2])
        temp_new_delta.append((temp_org, edge[1], temp_dest))
    new_delta = temp_new_delta

    temp_new_final_state = []
    for new_final_state in new_final_states:
        temp_new_final_state.append(''.join(new_final_state))
    new_final_states = temp_new_final_state

    new_initial_state = ''.join(new_initial_state)


    return (
        new_states, alphabet, new_delta, new_initial_state, new_final_states
    )


