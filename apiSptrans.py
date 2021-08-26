import requests

class SPTransClient(object):
    """ Um cliente python para a API Olho Vivo """

    session = requests.Session()
    url = 'http://api.olhovivo.sptrans.com.br/v2.1/'

    def auth(self, token):

        """
        Para autenticar-se no serviço de API do Olho Vivo
        é necessário efetuar uma chamada prévia utilizando
        o método http POST informando seu token de acesso.
        Essa chamada irá retornar true quando a autenticação
        for realizada com sucesso e false em caso de erros.
        """

        method = 'Login/Autenticar?token=%s' % token
        response = self.session.post(self.url + method)

        if response.cookies:
            return True

        return False

    def _get(self, path):

        """ HTTP GET comum para os demais métodos """

        response = self.session.get(self.url + path)
        data = response.json()
        return data

    def search_by_bus(self, term):

        """
        Realiza uma busca das linhas do sistema com base no
        parâmetro informado. Se a linha não é encontrada então
        é realizada uma busca fonetizada na denominação das linhas.
        """

        return self._get('Linha/Buscar?termosBusca=%s' % term)

    def get_bus_position(self, uid):

        """
        Retorna uma lista com todos os veículos de uma determinada linha
        com suas devidas posições.
        """

        return self._get('Posicao/Linha?codigoLinha=%s' % uid)
