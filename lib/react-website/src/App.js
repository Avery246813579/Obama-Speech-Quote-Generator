import React, {Component} from 'react';
import './App.css';
import logo from './hero.jpg';
import seal from './seal.png';

class Quote extends Component {
    render() {
        return (
            <div>
                {this.props.text}
            </div>
        )
    }
}

class Favorites extends Component {
    render() {
        return (
            <div>
                {this.props.favorites.map(function (item) {
                    return <p key={item.toString()}>- {item}</p>
                })}
            </div>
        )
    }
}

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {quote: "Filler Text", id: 0, favorites: ['Dogs', 'Cats']};
        this.refreshSentence = this.refreshSentence.bind(this);
        this.tweet = this.tweet.bind(this);
        this.componentWillMount = this.componentWillMount.bind(this);
        this.favorite = this.favorite.bind(this);

    }

    refreshSentence() {
        let self = this;

        fetch('http://127.0.0.1:5000/new', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify({test: ""})
        }).then((response) => response.json())
            .then(function (responseJson) {
                self.setState({quote: responseJson['data'], id: responseJson['id']});
            })
            .catch((error) => {
                console.log(error);
                alert("Internal Error" + JSON.stringify(error));
            });
    }

    tweet() {
        let self = this;

        fetch('http://127.0.0.1:5000/tweet', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify({tweet: self.state.id})
        }).then((response) => response.json())
            .then(function (responseJson) {
                alert("Tweet Successful");
            })
            .catch((error) => {
                alert("Internal Error!");
            });
    }

    favorite() {
        let self = this;

        fetch('http://127.0.0.1:5000/favorite_tweet', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify({tweet: self.state.id})
        }).then((response) => response.json())
            .then(function (responseJson) {
                let favorites = self.state.favorites;
                favorites.push(self.state.quote);

                self.setState({favorites: favorites});
            })
            .catch((error) => {
                alert("Internal Error!");
            });
    }

    componentWillMount() {
        this.refreshSentence();
        let self = this;

        fetch('http://127.0.0.1:5000/favorite_tweets', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        }).then((response) => response.json())
            .then(function (responseJson) {
                self.setState({favorites: responseJson['data']});
            })
            .catch((error) => {
                console.log(error);
                alert("Internal Error" + JSON.stringify(error));
            });
    }

    render() {
        return (
            <div id="wrapper">
                <div id="navbar" style={{margin: "auto", textAlign: "center", padding: "3px"}}>
                    <img src={seal} style={{maxHeight: "50px"}} alt="DOGS"/>
                </div>

                <img src={logo} style={{maxWidth: "100%"}} alt="logo"/>

                <div id="quote">
                    <div className="header">
                        Yes, we did. Yes, we can.
                    </div>

                    <div className="text">
                        <div id="sentence">
                            <Quote text={this.state.quote}/>
                        </div>

                        - President Barack Obama
                    </div>

                    <div className="buttons">
                        <a onClick={this.refreshSentence} className='button'>Generate a new quote</a>
                        <a onClick={this.tweet} className='button'>Tweet this quote</a>
                        <a onClick={this.favorite} className='button'>Favorite this quote</a>
                    </div>
                    <div className="buttons" style={{color: "white"}}>
                        Topic:&nbsp;

                        <select>
                            <option value="0">
                                Random
                            </option>
                            <option value="1">
                                America
                            </option>
                            <option>
                                China
                            </option>
                            <option>
                                Custom
                            </option>
                        </select>
                    </div>
                </div>

                <div id="about">
                    <div className="header">
                        AN IN-DEPTH LOOK AT THIS PROJECT
                    </div>
                    <br/>
                    <center><a href="https://github.com/Avery246813579/Obama-Speech-Quote-Generator">This project</a>
                        was made by <a
                            href="https://www.linkedin.com/in/avery-durrant-676402148/">Avery Durrant</a> using Markov
                        Chains.
                    </center>
                    <center>The Corpus I used was has a lot lines of text and a few words. It was taken from
                        over 200 of
                        Barack Obama's Speeches.
                    </center>

                    <div>
                        Favorites:
                    </div>
                    <div id="favorites">
                        <Favorites favorites={this.state.favorites}/>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
