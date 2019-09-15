import React from 'react'
import { Dimmer, Loader, Image, Segment } from 'semantic-ui-react'

const LoaderView = () => (
  <div>
    <Segment style={{ maxHeight: 450 }}>
      <Dimmer active>
        <Loader size='massive' inverted indeterminate>Servicing your preferences</Loader>
      </Dimmer>
    </Segment>
  </div>
)

export default LoaderView
